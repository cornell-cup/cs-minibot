"""
Test script for minibot movement
"""
from minibot.bot import Bot

import json

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

def run(bot):
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