from minibot.bot import Bot
import json

if __name__=="__main__":
    config_file = open("/home/pi/cs-minibot/minibot/configs/config.json")
    bot = Bot(json.loads(config_file.read()))
    print("Move Forward for 5 Seconds")
    bot.move_forward(20)
    bot.wait(5)
    print("Move Backward for 5 Seconds")
    bot.move_backward(20)
    bot.wait(5)
    bot.stop()
    print("Stopped!")
