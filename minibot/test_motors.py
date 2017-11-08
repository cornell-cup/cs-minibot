"""
Unit tests for minibot motors.
"""
from minibot.bot import Bot

import unittest
import json

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

class TestBotBasics(unittest.TestCase):
    """
    Tests basic functionalities of the minibot, such as movement and bot states.
    """
    def test_bot_motors(self):
        """
        Tests bot motors.
        """
        print("Initializing Minibot Software")
        config_file = open(CONFIG_LOCATION)
        config = json.loads(config_file.read())
        bot = Bot(config)
        print("Moving Forward - 3 seconds")
        bot.move_forward(50)
        bot.wait(3)
        print("Moving Backward - 3 seconds")
        bot.move_backward(50)
        bot.wait(3)
        print("Turning Left - 3 seconds")
        bot.turn_counter_clockwise(50)
        bot.wait(3)
        print("Turning Right - 3 seconds")
        bot.turn_clockwise(50)
        bot.wait(3)
        print("Stop")
        bot.stop()

if __name__ == "__main__":
    unittest.main()