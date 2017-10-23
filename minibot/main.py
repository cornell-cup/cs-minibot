"""
Something
"""

from minibot.bot import Bot
import json
import importlib

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

def main():
    print("Initializing Minibot Software")
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())
    bot = Bot(config)
    while True:
        bot.run()

if __name__ == "__main__":
    main()
