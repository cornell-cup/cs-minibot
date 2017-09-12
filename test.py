# Run all tests in this project

import os
import sys
import unittest

if __name__=="__main__":
    loader = unittest.TestLoader()
    tests = loader.discover(".", pattern="test_*.py")
    runner = unittest.TextTestRunner()
    runner.run(tests)
