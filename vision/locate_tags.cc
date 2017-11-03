#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <vector>
using namespace cv;
using std::vector;
int main(int argc, char** argv) {
    // Display usage
    if (argc < 2) {
        printf("Usage: %s [cameras...]\n", argv[0]);
        return -1;
    }
    // Parse arguments
    vector<VideoCapture> devices;
    vector<int> device_ids;
    vector<Mat> device_camera_matrix;
    vector<Mat> device_dist_coeffs;
    vector<Mat> cam_transforms;
    for (int i = 1; i < argc; i++) {
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
        Mat camera_matrix, dist_coeffs, cam_transform;
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
                dist_coeffs = Mat(data, true).reshape(1,1);//one row 5 cols
            }
            else if (key == "transform_matrix"){
                vector<double> data;
                for (int i = 0; i < 16; i++){
                  double v;
                  line_stream >> v;
                  data.push_back(v);
                }
                cam_transform = Mat(data, true).reshape(1,4);
            }
            else {
                std::cerr << "Unrecognized key '" << key << "' in file " << argv[i] << std::endl;
            }
        }
        if (camera_matrix.rows != 3 || camera_matrix.cols != 3) {
            std::cerr << "Error reading camera_matrix in file " << argv[i] << std::endl;
            continue;
        }

        if (dist_coeffs.rows != 3 || dist_coeffs.cols != 3) {
            std::cerr << "Error reading dist_coeffs in file " << argv[i] << std::endl;
            continue;
        }

        if (transform_matrix.rows != 4 || dist_coeffs.cols != 4){
            std::cerr << "Error reading transforms in file " << argv[i] << std::endl;
            continue;
        }

        device.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
        device.set(CV_CAP_PROP_FRAME_HEIGHT, 720);
        device.set(CV_CAP_PROP_FPS, 30);
        devices.push_back(device);
        device_ids.push_back(id);
        device_camera_matrix.push_back(camera_matrix);
        device_dist_coeffs.push_back(dist_coeffs);
        cam_transforms.push_back(cam_transform);
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
    while (key != 27) { // Quit on escape keypress
        for (size_t i = 0; i < devices.size(); i++) {
            if (!devices[i].isOpened()) {
                continue;
            }
            devices[i] >> frame;
            imshow(std::to_string(i), frame);
        }
        key = waitKey(16);
    }
}
