"""
Something
"""

from minibot.bot import Bot
import json
import importlib
from threading import Thread
from minibot.hardware.communication.TCP import TCP
import minibot.hardware.communication.UDP
import minibot
CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

def main():
    print("Initializing Minibot Software")
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())
    bot = Bot(config)

    tcpInstance = None
    tcpInstance = TCP()
    print(tcpInstance)
    thread_udp = Thread(target= minibot.hardware.communication.UDP.udpBeacon)
    thread_udp.start()    
    while True:
        tcpCmd = tcpInstance.get_command()

if __name__ == "__main__":
    main()
