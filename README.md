# MiniBot Platform

This repo is a test python implementation of MiniBot. Original repo can be found
[here](http://github.com/cornell-cup/cs-minibot-platform). This is a refactored
version.

Minibot is a modular robotics kit meant for children and students from age 6 - 18,
developed in partnership with DaVinci Robotics. This repository contains sample
scripts that allow users to run simple algorithms on their minibot, as well as
a simple web app that is a simple interface from which users can control the
minibot and send custom scripts.

This repository is currently in development.

Software resources:
 - Tornado
 - Google Blockly
 - Adafruit RPi libraries (TCS34725)

## Contributing to the Repository

Before working with the code, install pylint to use the Python linter.

```
pip install pylint
```

To run pylint on the code, run the following line from the root directory.

```
pylint minibot
```

Run pylint before committing or making pull requests so that code quality
can be maintained.

## Dependencies

### Developer Dependencies

Install the dependencies in `requirements.txt` and `requirements-rpi.txt`.
From the root directory, run the following line in terminal.

```
pip install -r requirements.txt
```

### Dependencies on the Rapsberry Pi

When SSH'ed into a minibot's Raspberry Pi, make sure to install the requirements for the RPi.

```
pip install -r requirements-rpi.txt
```

This is not necessary on your personal laptop or computer when developing, but is necessary
to run the hardware on the minibot when testing.

## Run the BaseStation

After all dependencies are successfully installed, you can run the BaseStation on your
computer and start working with the minibot.

The BaseStation is the intermediary that manages information flow between the minibot and
hardware to the software and GUI. BaseStation runs on `cs-minibot/gui/main.py` and is a
simple web application that runs on HTTP.

To run the BaseStation, run the following line in your terminal from your root directory.

```
python3 gui/main.py
```

Go to any browser on your computer and go to `localhost:1234/gui` to see the GUI in action.
If you are having trouble running the previous line, make sure that python3 is installed.
You can check this by typing `python3` in your terminal. If there is an error,
