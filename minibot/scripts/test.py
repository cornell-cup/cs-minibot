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
    # print("Moving Forward - 5 seconds")
    bot.move_forward(100)
    bot.wait(300)

if __name__=="__main__":
    run(None)
