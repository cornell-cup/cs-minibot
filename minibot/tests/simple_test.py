"""
Test script for minibot movement
"""

import json
from minibot.bot import Bot

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

def run():
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

if __name__=="__main__":
    run()