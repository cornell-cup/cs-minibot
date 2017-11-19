"""
Script which is automatically run on the MiniBot's Pi upon startup.
Must be configured in /etc/init.d/minibotinit.sh on the RPi.
"""

from minibot.bot import Bot
from minibot.hardware.communication.TCP import TCP
import minibot.hardware.communication.UDP

import importlib
import json
import time
import os
from multiprocessing import Process as Thread

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

class MiniBotProcess():
    def __init__(self, bot):
        self.bot = bot

    def parse_command(self, cmd):
        """
        Parses command sent by SendKV via TCP to the bot.
        Sent from BaseStation.

        Args:
             cmd (:obj:`str`): The command name.
             bot (:obj:`Bot`): Bot object to run the command on.
             p (:obj:`str`): Payload or contents of command.
        """
        global p
        comma = cmd.find(",")
        start = cmd.find("<<<<")
        end = cmd.find(">>>>")
        key = cmd[start + 4:comma]
        value = cmd[comma + 1:end]
        if key == "WHEELS":
            try:
                values = value.split(",")
                bot.set_wheel_power(int(values[0]), int(values[1]))
            except Exception as e:
                print(e)
                print("oh no!")
                pass
        elif key == "SCRIPT":
            user_script_file = open("/home/pi/cs-minibot/minibot/scripts/UserScript.py", 'w')
            val = process_string(value)
            user_script_file.write(val)
            user_script_file.close()
            p = self.spawn_script_process(p, self.bot)
        elif key == "RUN":
            filename = os.path.basename(value)
            filepath = "/home/pi/cs-minibot/minibot/scripts/" + filename
            print(filepath)
            if os.path.isfile(filepath):
                p = self.spawn_named_script_process(p, filename.split('.')[0])
            else:
                print("Invalid File path")

    def spawn_script_process(self, p):
        if (p is not None and p.is_alive()):
            p.terminate()
        time.sleep(0.1)
        p = Thread(target=self.run_script, args=[self.bot])
        p.start()
        # Return control to main after .1 seconds
        return p

    def spawn_named_script_process(self, p, script_name):
        if (p is not None and p.is_alive()):
            p.terminate()
        time.sleep(0.1)
        p = Thread(target=self.run_script_with_name, args=[self.bot, script_name])
        p.start()
        # Return control to main after .1 seconds
        return p

    def run_script_with_name(self, script_name):
        UserScript = importlib.import_module("scripts." + script_name)
        UserScript.run(self.bot)

    def run_script(self):
        from scripts import UserScript
        UserScript.run(self.bot)


p = None
def main():
    print("Initializing Minibot Software")
    p = None
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())

    # Initialize bot and TCP.
    bot = Bot(config)
    tcpInstance = TCP()
    print(tcpInstance)
    # Initialize thread.
    thread_udp = Thread(target=minibot.hardware.communication.UDP.udpBeacon)
    thread_udp.start()

    minibot_process = MiniBotProcess(bot)

    while True:
        tcpCmd = tcpInstance.get_command()
        minibot_process.parse_command(tcpCmd)
        time.sleep(0.01)


# Copy script sent from GUI into 'run' command
# So we can call that method to initiate the commands
def process_string(value):
    cmds = value.splitlines()
    str = "def run(bot):\n"
    for i in range(len(cmds)):
        str += "    " + cmds[i] + "\n"
    return str

if __name__ == "__main__":
    main()
