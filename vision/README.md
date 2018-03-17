# MiniBot Overhead Vision

## Dependencies

### OpenCV

Based on https://docs.opencv.org/3.1.0/d7/d9f/tutorial_linux_install.html.

```
# Install dependencies
sudo apt-get install build-essential cmake-gui
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

# Clone the OpenCV repositories and set the version to 3.3.0
cd ~
git clone https://github.com/opencv/opencv.git
cd opencv && git checkout 3.3.0 && cd ..
git clone https://github.com/opencv/opencv_contrib.git
cd opencv_contrib && git checkout 3.3.0 && cd ..

# Run cmake-gui
cmake-gui

# Set the source code path to ~/opencv
# Set the build path to ~/opencv/build
# Press Configure once or twice
# Check the "Advanced" box
# In the options, enable BUILD_opencv_world
# In the options, set OPENCV_EXTRA_MODULES_PATH to /home/cornellcup/opencv_contrib/modules
# Press Configure one more time
# Press Generate

# Build OpenCV
cd opencv/build
make -j4

# Install
sudo make install
```

### AprilTags

From https://april.eecs.umich.edu/software/apriltag.html.
```
# Download and extract the source
wget https://april.eecs.umich.edu/media/apriltag/apriltag-2016-12-01.tgz
tar xvf apriltag-2016-12-01.tgz
cd apriltag-2016-12-01

# Build and install
make
sudo make install
```

### Vision

```
# In the cs-minibot repo
cd vision
make
```

## Usage

### Adding variables to LD_LIBRARY_PATH

```
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

### Calibrating the cameras

Print out a checkerboard and tape / paste it to a flat surface.

### Locating the cameras relative to the 0 tag


### Locating tags and sending them to the basestation
