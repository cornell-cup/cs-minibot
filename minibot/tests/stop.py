from minibot.bot import Bot
import json

if __name__=="__main__":
    config_file = open("/home/pi/cs-minibot/minibot/configs/config.json")
    bot = Bot(json.loads(config_file.read())
    bot.move_forward(20)
