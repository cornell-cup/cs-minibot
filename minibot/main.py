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

# Location of config file which contains hardware pin info about
# bot peripherals, etc.
CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

def main():
    """
    Main method. Initializes communication methods and MiniBot object
    (configures hardware components to software). Sets up TCP listener
    for commands from BaseStation.
    """

    print("Initializing Minibot Software")
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())

    # Bot and TCP initialization.
    bot = Bot(config)
    tcpInstance = TCP()
    print(tcpInstance)

    # Initializing UDP thread.
    thread_udp = Thread(target= minibot.hardware.communication.UDP.udpBeacon)
    thread_udp.start()    

    while True:
        # Listen for TCP commands from BaseStation.
        tcpCmd = tcpInstance.get_command()
        bot.parse_command(tcpCmd, tcpInstance)
        time.sleep(0.01)

if __name__ == "__main__":
    main()
