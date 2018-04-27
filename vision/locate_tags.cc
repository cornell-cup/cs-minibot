#include <apriltag/apriltag.h>
#include <apriltag/tag36h11.h>
#include <apriltag/tag36artoolkit.h>
#include <curl/curl.h>
#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <fstream>

using namespace cv;
using std::vector;

#define TAG_SIZE 6.5f
#define PI acos(-1)


int main(int argc, char** argv) {
	// Display usage
	if (argc < 3) {
		printf("Usage: %s <basestation url> [cameras...]\n", argv[0]);
		return -1;
	}
	// Parse arguments
	CURL *curl;
	curl = curl_easy_init();
	if (!curl) {
		std::cerr << "Failed to initialize curl" << std::endl;
		return -1;
	}
	curl_easy_setopt(curl, CURLOPT_URL, argv[1]);
	curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 200L);

	vector<VideoCapture> devices;
	vector<int> device_ids;
	vector<Mat> device_camera_matrix;
	vector<Mat> device_dist_coeffs;
	vector<Mat> device_transform_matrix;
	for (int i = 2; i < argc; i++) {
		int id = atoi(argv[i]);
		VideoCapture device(id);
		if (!device.isOpened()) {
			std::cerr << "Failed to open video capture device " << id << std::endl;
			continue;
		}
		std::ifstream fin;
		fin.open(argv[i]);
		if (fin.fail()) {
			std::cerr << "Failed to open file " << argv[i] << std::endl;
			continue;
		}
		Mat camera_matrix, dist_coeffs, transform_matrix;
		std::string line;
		// TODO Error checking
		while (std::getline(fin, line)) {
			std::stringstream line_stream(line);
			std::string key, equals;
			line_stream >> key >> equals;
			if (key == "camera_matrix") {
				vector<double> data;
				for (int i = 0; i < 9; i++) {
					double v;
					line_stream >> v;
					data.push_back(v);
				}
				camera_matrix = Mat(data, true).reshape(1,3);
			}
			else if (key == "dist_coeffs") {
				vector<double> data;
				for (int i = 0; i < 5; i++) {
					double v;
					line_stream >> v;
					data.push_back(v);
				}
				dist_coeffs = Mat(data, true).reshape(1,1);
			}
			else if (key == "transform_matrix"){
				vector<double> data;
				for (int i = 0; i < 16; i++){
				  double v;
				  line_stream >> v;
				  data.push_back(v);
				}
				transform_matrix = Mat(data, true).reshape(1,4);
			}
			else {
				std::cerr << "Unrecognized key '" << key << "' in file " << argv[i] << std::endl;
			}
		}
		if (camera_matrix.rows != 3 || camera_matrix.cols != 3) {
			std::cerr << "Error reading camera_matrix in file " << argv[i] << std::endl;
			continue;
		}

		if (dist_coeffs.rows != 1 || dist_coeffs.cols != 5) {
			std::cerr << "Error reading dist_coeffs in file " << argv[i] << std::endl;
			continue;
		}

		if (transform_matrix.rows != 4 || transform_matrix.cols != 4){
			std::cerr << "Error reading transform_matrix in file " << argv[i] << std::endl;
			continue;
		}

		device.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
		device.set(CV_CAP_PROP_FRAME_HEIGHT, 720);
		device.set(CV_CAP_PROP_FPS, 30);
		devices.push_back(device);
		device_ids.push_back(id);
		device_camera_matrix.push_back(camera_matrix);
		device_dist_coeffs.push_back(dist_coeffs);
		device_transform_matrix.push_back(transform_matrix);
	}
	// Initialize detector
	apriltag_family_t* tf = tag36h11_create();
	tf->black_border = 1;
	apriltag_detector_t* td = apriltag_detector_create();
	apriltag_detector_add_family(td, tf);
	td->quad_decimate = 1.0;
	td->quad_sigma = 0.0;
	td->nthreads = 4;
	td->debug = 0;
	td->refine_edges = 1;
	td->refine_decode = 0;
	td->refine_pose = 0;
	int key = 0;
	Mat frame, gray;
	char postDataBuffer[100];

	float cameraCoordinates[(int)devices.size()*3]; // For each camera i, x coordinate saved at index i*3, y at index i*3+1, z at i*3+2
	float cam2originAngles[(int)devices.size()]; // For each camera i, the angle between the camera and the origin's normal vector is saved at index i

	for (size_t i = 0; i < devices.size(); i++) {
		if (!devices[i].isOpened()) {
			continue;
		}

		// get the coordinates of the camera
		vector<double> zeroVector;
		zeroVector.push_back(0);
		zeroVector.push_back(0);
		zeroVector.push_back(0);
		zeroVector.push_back(1);
		Mat zero = Mat(zeroVector,true).reshape(1, 4);
		Mat cameraXYZS = device_transform_matrix[i] * zero;
		cameraCoordinates[i*3] = cameraXYZS.at<double>(0);
		cameraCoordinates[i*3+1] = cameraXYZS.at<double>(1);
		cameraCoordinates[i*3+2] = cameraXYZS.at<double>(2);

		// get angle between camera and origin's normal vector
		float originToCameraVector[3];
		// Use vector from Camera to Origin
			// originToCameraVector[0] = cameraCoordinates[i*3];
			// originToCameraVector[1] = cameraCoordinates[i*3+1];
			// originToCameraVector[2] = cameraCoordinates[i*3+2];
		// Use <0,0,1>
			originToCameraVector[0] = 0;
			originToCameraVector[1] = 0;
			originToCameraVector[2] = 1;
		Mat origin2cam = device_transform_matrix[i].inv();
		float originrpy[3];
		originrpy[0] = asin(origin2cam.at<double>(2,0));
		originrpy[1] = atan2(origin2cam.at<double>(2,1), origin2cam.at<double>(2,2));
		originrpy[2] = atan2(origin2cam.at<double>(1,0), origin2cam.at<double>(0,0)); 
		float originNormalVector[3];
		originNormalVector[0] = 0;
		originNormalVector[1] = 0;
		originNormalVector[2] = 1;
		float x0, y0, z0;
		// http://danceswithcode.net/engineeringnotes/rotations_in_3d/rotations_in_3d_part1.html
		// apply roll
		x0 = originNormalVector[0];
		y0 = originNormalVector[1];
		z0 = originNormalVector[2];
		originNormalVector[1] = y0*cos(originrpy[0]) - z0*sin(originrpy[0]);
		originNormalVector[2] = y0*sin(originrpy[0]) + z0*cos(originrpy[0]);
		// apply pitch
		x0 = originNormalVector[0];
		y0 = originNormalVector[1];
		z0 = originNormalVector[2];			 
		originNormalVector[0] = x0*cos(originrpy[1]) + z0*sin(originrpy[1]);
		originNormalVector[2] = z0*cos(originrpy[1]) - x0*sin(originrpy[1]);
		float dotProduct = originToCameraVector[0]*originNormalVector[0] + originToCameraVector[1]*originNormalVector[1] + originToCameraVector[2]*originNormalVector[2];
		float mag1 = sqrt(pow(originToCameraVector[0],2) + pow(originToCameraVector[1],2) + pow(originToCameraVector[2],2));
		float mag2 = sqrt(pow(originNormalVector[0],2) + pow(originNormalVector[1],2) + pow(originNormalVector[2],2));
		cam2originAngles[i] = acos(dotProduct / (mag1 * mag2));
		if(cam2originAngles[i] > PI/2)
			cam2originAngles[i] = PI - cam2originAngles[i];

	}

	// create the file to save data to
	std::ofstream outputFile;
	outputFile.open("output.txt", std::ofstream::out | std::ofstream::app);

	while (key != 27) { // Quit on escape keypress

		// map to store weighted coordinates [x, y, z, roll, pitch, yaw, total weight]
		// weightings are based on distance from camera to tag and angle between camera and origin's normal vector
		std::map <int, float[7]> weightedCoords;

		if(key == 'w') {
			time_t _tm =time(NULL );
			struct tm * curtime = localtime ( &_tm );
			outputFile << asctime(curtime);
		}

		for (size_t i = 0; i < devices.size(); i++) {
			if (!devices[i].isOpened()) {
				continue;
			}

			devices[i] >> frame;
			cvtColor(frame, gray, COLOR_BGR2GRAY);
			image_u8_t im = {
				.width = gray.cols,
				.height = gray.rows,
				.stride = gray.cols,
				.buf = gray.data
			};

			zarray_t* detections = apriltag_detector_detect(td, &im);			
			vector<Point2f> img_points(4);
		 	vector<Point3f> obj_points(4);
		   	Mat rvec(3, 1, CV_64FC1);
			Mat tvec(3, 1, CV_64FC1);

			printf("~~~~~~~~~~~~~ Camera %d ~~~~~~~~~~~~\n", (int)i);
			printf("Coordinates: (%f, %f, %f)\n", cameraCoordinates[i*3], cameraCoordinates[i*3+1], cameraCoordinates[i*3+2]);
			printf("Cam to Origin Angle: %f\n", cam2originAngles[i] *180/PI);

			if (key == 'w')
				outputFile 
					<< "~~~~~~~~~~~~~ Camera " << i << " ~~~~~~~~~~~~\n" 
					<< "Coordinates: (" << cameraCoordinates[i*3] << ", " << cameraCoordinates[i*3+1] << ", " << cameraCoordinates[i*3+2] << ")\n"
					<< "Cam to Origin Angle: " << cam2originAngles[i]*180/PI << "\n";


			for (int j = 0; j < zarray_size(detections); j++) {
	
				// Get the ith detection
				apriltag_detection_t *det;
				zarray_get(detections, j, &det);

				// Draw onto the frame
				line(frame, Point(det->p[0][0], det->p[0][1]),
						 Point(det->p[1][0], det->p[1][1]),
						 Scalar(0, 0xff, 0), 2);
				line(frame, Point(det->p[0][0], det->p[0][1]),
						 Point(det->p[3][0], det->p[3][1]),
						 Scalar(0, 0, 0xff), 2);
				line(frame, Point(det->p[1][0], det->p[1][1]),
						 Point(det->p[2][0], det->p[2][1]),
						 Scalar(0xff, 0, 0), 2);
				line(frame, Point(det->p[2][0], det->p[2][1]),
						 Point(det->p[3][0], det->p[3][1]),
						 Scalar(0xff, 0, 0), 2);

				// Compute transformation using PnP
				img_points[0] = Point2f(det->p[0][0], det->p[0][1]);
				img_points[1] = Point2f(det->p[1][0], det->p[1][1]);
				img_points[2] = Point2f(det->p[2][0], det->p[2][1]);
				img_points[3] = Point2f(det->p[3][0], det->p[3][1]);

				obj_points[0] = Point3f(-TAG_SIZE * 0.5f, -TAG_SIZE * 0.5f, 0.f);
				obj_points[1] = Point3f( TAG_SIZE * 0.5f, -TAG_SIZE * 0.5f, 0.f);
				obj_points[2] = Point3f( TAG_SIZE * 0.5f,  TAG_SIZE * 0.5f, 0.f);
				obj_points[3] = Point3f(-TAG_SIZE * 0.5f,  TAG_SIZE * 0.5f, 0.f);

				solvePnP(obj_points, img_points, device_camera_matrix[i],
						device_dist_coeffs[i], rvec, tvec);
				Matx33d r;
				Rodrigues(rvec,r);

				vector<double> data;
				data.push_back(r(0,0));
				data.push_back(r(0,1));
				data.push_back(r(0,2));
				data.push_back(tvec.at<double>(0));
				data.push_back(r(1,0));
				data.push_back(r(1,1));
				data.push_back(r(1,2));
				data.push_back(tvec.at<double>(1));
				data.push_back(r(2,0));
				data.push_back(r(2,1));
				data.push_back(r(2,2));
				data.push_back(tvec.at<double>(2));
				data.push_back(0);
				data.push_back(0);
				data.push_back(0);
				data.push_back(1);
				Mat tag2cam = Mat(data,true).reshape(1, 4);

				vector<double> zeroVector;
				zeroVector.push_back(0);
				zeroVector.push_back(0);
				zeroVector.push_back(0);
				zeroVector.push_back(1);
				Mat genout = Mat(zeroVector,true).reshape(1, 4);

				Mat tag2orig = device_transform_matrix[i] * tag2cam;
				Mat tagXYZS = tag2orig * genout;

				// compute roll, pitch, and yaw
			 
				float rpy[3];
				rpy[0] = asin(tag2orig.at<double>(2,0));
				rpy[1] = atan2(tag2orig.at<double>(2,1), tag2orig.at<double>(2,2));
				rpy[2] = atan2(tag2orig.at<double>(1,0), tag2orig.at<double>(0,0));		 

				// compute distance from camera to tag
				
				float xDistance = cameraCoordinates[i*3]-tagXYZS.at<double>(0);
				float yDistance = cameraCoordinates[i*3+1]-tagXYZS.at<double>(1);
				float zDistance = cameraCoordinates[i*3+2]-tagXYZS.at<double>(2);
				float distance  = sqrt(pow(xDistance,2) + pow(yDistance,2) + pow(zDistance,2));

				float weight = cos(cam2originAngles[i])/distance;
				
				// print out results

				printf("----Tag %d\n", det->id);
				printf("xyz: (%3.3f,%3.3f,%3.3f)\n", tagXYZS.at<double>(0), tagXYZS.at<double>(1), tagXYZS.at<double>(2));
				printf("rpy: (%3.3f,%3.3f,%3.3f)\n", rpy[0]*180/PI, rpy[1]*180/PI, rpy[2]*180/PI);
				printf("Dist, Angle, Weight: (%3.3f, %3.3f, %3.3f)\n", distance, cam2originAngles[i]*180/PI, weight*100);
				
				if (key == 'w') {
					char* output = (char*)malloc(100);
					sprintf(output,"----Tag %d\n", det->id);
					outputFile << output;
					sprintf(output, "xyz: (%3.3f,%3.3f,%3.3f)\n", tagXYZS.at<double>(0), tagXYZS.at<double>(1), tagXYZS.at<double>(2));
					outputFile << output;
					sprintf(output, "rpy: (%3.3f,%3.3f,%3.3f)\n", rpy[0]*180/PI, rpy[1]*180/PI, rpy[2]*180/PI);
					outputFile << output;
					sprintf(output, "Dist, Angle, Weight: (%3.3f, %3.3f, %3.3f)\n", distance, cam2originAngles[i]*180/PI, weight*100);
					outputFile << output;
					free(output);
				}

				// sava distances in weighted coords map

				weightedCoords[det->id][0] += tagXYZS.at<double>(0)*weight;
				weightedCoords[det->id][1] += tagXYZS.at<double>(1)*weight;
				weightedCoords[det->id][2] += tagXYZS.at<double>(2)*weight;
				weightedCoords[det->id][3] += rpy[0]*weight;
				weightedCoords[det->id][4] += rpy[1]*weight;
				weightedCoords[det->id][5] += rpy[2]*weight;
				weightedCoords[det->id][6] += weight;

				// Send data to basestation - incomplete
				sprintf(postDataBuffer, "{\"id\":%d,\"x\":%f,\"y\":%f,\"z\":%f}",
								det->id, tagXYZS.at<double>(0), tagXYZS.at<double>(1), tagXYZS.at<double>(2));
				curl_easy_setopt(curl, CURLOPT_POSTFIELDS, postDataBuffer);
				// TODO Check for error response
				curl_easy_perform(curl);
			}

			zarray_destroy(detections);

			imshow(std::to_string(i), frame);
		}

		printf("~~~~~~~~~~~~~ Overall Weighted Readings ~~~~~~~~~~~~\n");
		if (key == 'w')
			outputFile << "~~~~~~~~~~~~~ Overall Weighted Readings ~~~~~~~~~~~~\n";

		std::map<int, float[7]>::iterator it = weightedCoords.begin();

		while (it != weightedCoords.end()) {
			printf("----Tag %d\n", it->first);
			printf("xyz: (%3.3f,%3.3f,%3.3f)\n", it->second[0]/it->second[6], it->second[1]/it->second[6], it->second[2]/it->second[6]);
			printf("rpy: (%3.3f,%3.3f,%3.3f)\n", it->second[3]/it->second[6]*180/PI, it->second[4]/it->second[6]*180/PI, it->second[5]/it->second[6]*180/PI); 
			
			if (key == 'w') {
				char* output = (char*)malloc(100);
				sprintf(output, "----Tag %d\n", it->first);
				outputFile << output;
				sprintf(output, "xyz: (%3.3f,%3.3f,%3.3f)\n", it->second[0]/it->second[6], it->second[1]/it->second[6], it->second[2]/it->second[6]);
				outputFile << output;
				sprintf(output, "rpy: (%3.3f,%3.3f,%3.3f)\n", it->second[3]/it->second[6]*180/PI, it->second[4]/it->second[6]*180/PI, it->second[5]/it->second[6]*180/PI); 
				outputFile << output;
				free(output);
			}


			it++;
		}
		printf("==============================================\n");

		if (key == 'w') {
			char* output = (char*)malloc(100);
			sprintf(output,"==============================================\n");
			outputFile << output;	
			free(output);
			printf("Wrote to file: \"output.txt\"\n");
		}

		key = waitKey(16);
	}

	curl_easy_cleanup(curl);

	outputFile << "\n\n";
	outputFile.close();
}
