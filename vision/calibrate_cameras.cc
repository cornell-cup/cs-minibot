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
    for (int i = 4; i < argc; i++) {
        int id = atoi(argv[i]);
        VideoCapture device(id);
        if (device.isOpened()) {
            devices.push_back(device);
            device.set(CV_CAP_PROP_FRAME_WIDTH, 1280);
            device.set(CV_CAP_PROP_FRAME_HEIGHT, 720);
        }
        else {
            std::cerr << "Failed to open video capture device " << id << std::endl;
        }
    }

    Mat frame, gray;
    while (true) {
        for (size_t i = 0; i < devices.size(); i++) {
            devices[i] >> frame;
            imshow(std::to_string(i), frame);
        }

        // Quit on escape keypress
        if (waitKey(16) >= 27) {
            break;
        }
    }
}
