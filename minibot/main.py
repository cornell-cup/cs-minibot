"""
Script which is automatically run on the MiniBot's Pi upon startup.
Must be configured in /etc/init.d/minibotinit.sh on the RPi.
"""

from minibot.bot import Bot
from minibot.hardware.communication.TCP import TCP
import minibot.hardware.communication.UDP

import json
from threading import Thread
import time
import importlib

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

def main():
    print("Initializing Minibot Software")
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())
    bot = Bot(config)
    bot.motors.set_speed(1, 0)
    tcpInstance = TCP()
    print(tcpInstance)
    thread_udp = Thread(target= minibot.hardware.communication.UDP.udpBeacon)
    thread_udp.start()    
    while True:
        tcpCmd = tcpInstance.get_command()
        parse_command(tcpCmd, bot)
        time.sleep(0.01)

def parse_command(cmd, bot):
    """
    Parses command sent by SendKV via TCP to the bot.
    Sent from BaseStation.

    Args:
         cmd (:obj:`str`): The command name.
         bot (:obj:`Bot`): Bot object to run the command on.
         p (:obj:`str`): Payload or contents of command.
    """
    comma = cmd.find(",")
    start = cmd.find("<<<<")
    end = cmd.find(">>>>")
    key = cmd[start + 4:comma]
    value = cmd[comma + 1:end]
    if key == "WHEELS":
        try:
            values = value.split(",")
            bot.motors.set_speed(int(values[0])/100., int(values[1])/100.)
        except Exception as e:
            print(e)
            print("oh no!")
            pass

if __name__ == "__main__":
    main()
