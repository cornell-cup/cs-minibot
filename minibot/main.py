"""
Something
"""

from minibot.bot import Bot

CONFIG_LOCATION = 'configs/config.json'

def main():
    print("Initializing Minibot Software")
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())
    bot = Bot(config)

if __name__ == "__main__":
    main()