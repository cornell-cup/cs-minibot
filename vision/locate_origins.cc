#include <apriltag/apriltag.h>
#include <apriltag/tag36h11.h>
#include <apriltag/tag36artoolkit.h>
#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <stack>

using namespace cv;
using std::vector;
using std::stack;

#define TAG_SIZE 6.5f



vector<VideoCapture> devices;
vector<int> device_ids;
vector<Mat> device_camera_matrix;
vector<Mat> device_dist_coeffs;

Mat transrotationalmat(apriltag_detection_t *det1, apriltag_detection_t *det2,int device);

int main(int argc, char** argv) {
    // Display usage
    if (argc < 2) {
        printf("Usage: %s [cameras...]\n", argv[0]);
        return -1;
    }


    for (int i = 1; i < argc; i++) {
        int id = atoi(argv[i]);
        VideoCapture device(id);
        if (!device.isOpened()) {
            std::cerr << "Failed to open video capture device " << id << std::endl;
            continue;
        }

        Mat camera_matrix, dist_coeffs;
        std::ifstream fin;
        fin.open(argv[i]);
        if (fin.fail()) {
            std::cerr << "Failed to open file " << argv[i] << std::endl;
            continue;
        }

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
                camera_matrix = Mat(data, true).reshape(1, 3);
            }
            else if (key == "dist_coeffs") {
                vector<double> data;
                for (int i = 0; i < 5; i++) {
                    double v;
                    line_stream >> v;
                    data.push_back(v);
                }
                dist_coeffs = Mat(data, true).reshape(1, 1);
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

        device.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
        device.set(CV_CAP_PROP_FRAME_HEIGHT, 720);
        device.set(CV_CAP_PROP_FPS, 30);

        devices.push_back(device);
        device_ids.push_back(id);
        device_camera_matrix.push_back(camera_matrix);
        device_dist_coeffs.push_back(dist_coeffs);
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

    Mat frame, gray;
    std::unordered_map<int,Mat> tagmap;

    vector<double> data;
    data.push_back(1);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    data.push_back(1);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    data.push_back(1);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    data.push_back(1);
    Mat identity = Mat(data,true).reshape(1,4);
    tagmap.insert(std::make_pair(0,identity));

    stack<int> nextvisit;
    nextvisit.push(0);
    int currentTag;
    while (nextvisit.size() > 0) { // Quit on escape keypress
        currentTag = nextvisit.top();
        nextvisit.pop();
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
            bool contains = false;
            apriltag_detection_t *currdet;
            for (int j = 0; j < zarray_size(detections); j++) {
                // Get the ith detection
                apriltag_detection_t *det;
                zarray_get(detections, j, &det);
                if(det->id == currentTag){
                  currdet = det;
                  contains=true;
                }
            }
            printf("Accessed device %d",i);
            if(contains){
              printf("Entered with %d",zarray_size(detections));
              for (int j = 0; j < zarray_size(detections); j++) {
                  // Get the ith detection
                  apriltag_detection_t *det;
                  zarray_get(detections, j, &det);
                  if(det->id == currentTag){
                    continue;
                  }
                  std::unordered_map<int,Mat>::iterator iter;
                  iter = tagmap.find(det -> id);
                  if(iter != tagmap.end()){
                    tagmap.insert(std::make_pair(det ->id,transrotationalmat(currdet,det,i)));
                    nextvisit.push(det->id);
                    printf("Added new visits %d",(det-> id));
                  }
              }
            }



            zarray_destroy(detections);
            }



        }
        printf("\nsearch phase completed found %d tags\n",tagmap.size());

        for(auto it: tagmap){
          vector<double> data2;
          data2.push_back(0);
          data2.push_back(0);
          data2.push_back(0);
          data2.push_back(1);
          Mat genout = Mat(data2,true).reshape(1,4);
          printf("\n======== Tag %d ========\n",it.first);
          Mat camcoords = it.second * genout;

          printf("%zu :: filler :: % 3.3f % 3.3f % 3.3f\n", it.first,
                  camcoords.at<double>(0,0), camcoords.at<double>(1,0), camcoords.at<double>(2,0));

        }
        // for(int i = 0; i < tagmap.size(); i++){
        //   vector<double> data2;
        //   data2.push_back(0);
        //   data2.push_back(0);
        //   data2.push_back(0);
        //   data2.push_back(1);
        //   Mat genout = Mat(data2,true).reshape(1,4);
        //   Mat tag2origin = tagmap.find();
        //
        //   auto search = tagmap.find(i);
        //   if(search != example.end()) {
        //       std::cout << "Found " << search->first << " " << search->second << '\n';
        //   }
        //   else {
        //       std::cout << "Not found\n";
        //   }
        //   Mat camcoords = cam2origin * genout;
        //
        //   printf("%zu :: filler :: % 3.3f % 3.3f % 3.3f\n", i,
        //           camcoords.at<double>(0,0), camcoords.at<double>(1,0), camcoords.at<double>(2,0));
        //
        //   printf("Found tag %d at location ",tagmap.);
        // }
      // printf("written to camera %zu\n",i);
      // std::ofstream fout;
      // fout.open(std::to_string(device_ids[i]) + ".calib", std::ofstream::out);
      // fout << "camera_matrix =";
      // for (int r = 0; r < device_camera_matrix[i].rows; r++) {
      //     for (int c = 0; c < device_camera_matrix[i].cols; c++) {
      //         fout << " " << device_camera_matrix[i].at<double>(r, c);
      //     }
      // }
      // fout << std::endl;
      // fout << "dist_coeffs =";
      // for (int r = 0; r < device_dist_coeffs[i].rows; r++) {
      //     for (int c = 0; c < device_dist_coeffs[i].cols; c++) {
      //         fout << " " << device_dist_coeffs[i].at<double>(r, c);
      //     }
      // }
      // fout << std::endl;
      // fout << "transform_matrix =";
      // for (int r = 0; r < cam2origin.rows; r++) {
      //     for (int c = 0; c < cam2origin.cols; c++) {
      //         fout << " " << cam2origin.at<double>(r, c);
      //     }
      // }
      // fout << std::endl;
      // fout.close();
}
Mat transrotationalmat(apriltag_detection_t *det1,apriltag_detection_t *det2, int device){
  // Compute transformation using PnP
  vector<Point2f> img_points(4);
  vector<Point3f> obj_points(4);

  Mat rvec(3, 1, CV_64FC1);
  Mat tvec(3, 1, CV_64FC1);


  img_points[0] = Point2f(det1->p[0][0], det1->p[0][1]);
  img_points[1] = Point2f(det1->p[1][0], det1->p[1][1]);
  img_points[2] = Point2f(det1->p[2][0], det1->p[2][1]);
  img_points[3] = Point2f(det1->p[3][0], det1->p[3][1]);

  obj_points[0] = Point3f(-TAG_SIZE * 0.5f, -TAG_SIZE * 0.5f, 0.f);
  obj_points[1] = Point3f( TAG_SIZE * 0.5f, -TAG_SIZE * 0.5f, 0.f);
  obj_points[2] = Point3f( TAG_SIZE * 0.5f,  TAG_SIZE * 0.5f, 0.f);
  obj_points[3] = Point3f(-TAG_SIZE * 0.5f,  TAG_SIZE * 0.5f, 0.f);

  solvePnP(obj_points, img_points, device_camera_matrix[device],
          device_dist_coeffs[device], rvec, tvec);
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
  Mat tag12cam = Mat(data,true).reshape(1, 4);
  Mat cam2tag1 = tag12cam.inv();

  // Compute transformation using PnP
  img_points[0] = Point2f(det2->p[0][0], det2->p[0][1]);
  img_points[1] = Point2f(det2->p[1][0], det2->p[1][1]);
  img_points[2] = Point2f(det2->p[2][0], det2->p[2][1]);
  img_points[3] = Point2f(det2->p[3][0], det2->p[3][1]);

  obj_points[0] = Point3f(-TAG_SIZE * 0.5f, -TAG_SIZE * 0.5f, 0.f);
  obj_points[1] = Point3f( TAG_SIZE * 0.5f, -TAG_SIZE * 0.5f, 0.f);
  obj_points[2] = Point3f( TAG_SIZE * 0.5f,  TAG_SIZE * 0.5f, 0.f);
  obj_points[3] = Point3f(-TAG_SIZE * 0.5f,  TAG_SIZE * 0.5f, 0.f);

  solvePnP(obj_points, img_points, device_camera_matrix[device],
          device_dist_coeffs[device], rvec, tvec);
  Matx33d r1;
  Rodrigues(rvec,r1);

  vector<double> data2;
  data2.push_back(r1(0,0));
  data2.push_back(r1(0,1));
  data2.push_back(r1(0,2));
  data2.push_back(tvec.at<double>(0));
  data2.push_back(r1(1,0));
  data2.push_back(r1(1,1));
  data2.push_back(r1(1,2));
  data2.push_back(tvec.at<double>(1));
  data2.push_back(r1(2,0));
  data2.push_back(r1(2,1));
  data2.push_back(r1(2,2));
  data2.push_back(tvec.at<double>(2));
  data2.push_back(0);
  data2.push_back(0);
  data2.push_back(0);
  data2.push_back(1);
  Mat tag22cam = Mat(data2,true).reshape(1, 4);
  return cam2tag1*tag22cam;
}
