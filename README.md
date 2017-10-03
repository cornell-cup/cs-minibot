# M i n i B o t   P l a t f o r m

This repo is a test python implementation of MiniBot. Original repo can be found
[here](http://github.com/cornell-cup/cs-minibot-platform). This is a refactored
version.

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

When SSH'ed into a minibot's Raspberry Pi, make sure to `pip install -r requirements-rpi.txt`.
This is not necessary on your personal laptop or computer when developing, but is necessary
to run the hardware on the minibot when testing.
