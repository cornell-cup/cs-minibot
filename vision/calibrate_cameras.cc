#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

using namespace cv;
using std::vector;

int main(int argc, char** argv) {
    // Display usage
    if (argc < 5) {
        printf("Usage: %s <rows> <cols> <size> [cameras...]\n", argv[0]);
        return -1;
    }

    // Parse arguments
    int rows = atoi(argv[1]);
    int cols = atoi(argv[2]);
    float size = atof(argv[3]);

    // Open video capture devices
    vector<VideoCapture> devices;
    vector<vector<Point2f>> img_points;
    for (int i = 4; i < argc; i++) {
        int id = atoi(argv[i]);
        VideoCapture device(id);
        if (device.isOpened()) {
            devices.push_back(device);
            device.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
            device.set(CV_CAP_PROP_FRAME_HEIGHT, 720);
            device.set(CV_CAP_PROP_FPS, 30);
            img_points.push_back(vector<Point2f>());
        }
        else {
            std::cerr << "Failed to open video capture device " << id << std::endl;
        }
    }

    // Calibration variables
    Size checkerboard_size(cols, rows);

    int key = 0;
    Mat frame, gray;
    vector<Point2f> corners;
    while (key != 27) { // Quit on escape keypress
        for (size_t i = 0; i < devices.size(); i++) {
            devices[i] >> frame;

            // Detect checkerboards on spacebar
            if (waitKey(1) == 32) {
                cvtColor(frame, gray, COLOR_BGR2GRAY);
                bool found = findChessboardCorners(gray, checkerboard_size, corners);
                if (found) {
                    std::cout << "Found checkerboard on " << i << std::endl;
                    img_points[i].insert(
                            std::end(img_points[i]), std::begin(corners), std::end(corners));
                    cornerSubPix(gray, corners, Size(11, 11), Size(-1, -1),
                            TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 30, 0.1));
                }
                drawChessboardCorners(frame, checkerboard_size, Mat(corners), found);
            }

            imshow(std::to_string(i), frame);
        }

        key = waitKey(16);
        if (key == 'W') { // Write calibration to text files
            std::cout << "TODO Write to output" << std:: endl;
        }
    }
}
