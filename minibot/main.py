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
from threading import Thread

class MiniBotProcess():
    """
    Minibot Process class. Given a bot, it will parse incoming
    commands from basestation and run it on that bot. This is a
    1:1 correlation, since each MiniBot's RPi will be individually
    running this file.

    Args:
        bot (obj:`Bot`): MiniBot object which will be running scripts
            sent to it through TCP commands from the BaseStation.
    """
    def __init__(self, bot):
        # Bot object.
        self.bot = bot

        # Thread object.
        self.p = None

    def parse_command(self, cmd):
        """
        Parses command sent by SendKV via TCP to the bot.
        Sent from BaseStation.

        Args:
             cmd (:obj:`str`): The command name.
             bot (:obj:`Bot`): Bot object to run the command on.
             p (:obj:`str`): Payload or contents of command.
        """
        key, value = process_payload(cmd)

        if key == "WHEELS":
            try:
                values = value.split(",")
                self.bot.set_wheel_power(int(values[0]), int(values[1]))
            except Exception as e:
                print(e)
                print("oh no!")
                pass

        elif key == "SCRIPT":
            # Inserts user's script into UserScript.py file.
            print("Script command received!")
            user_script_file = open("/home/pi/cs-minibot/minibot/scripts/UserScript.py", 'w')

            val = process_string(value)
            print("Value: \n", val)
            user_script_file.write(val)
            user_script_file.close()

            # Runs user's script that is now in the dummy file.
            self.p = self.spawn_script_process()

        elif key == "RUN":
            # Finds named file within minibot's scripts directory.
            filename = os.path.basename(value)
            filepath = "/home/pi/cs-minibot/minibot/scripts/" + filename
            print(filepath)

            # If file is found, run it.
            if os.path.isfile(filepath):
                self.p = self.spawn_named_script_process(filename.split('.')[0])
            else:
                print("Invalid File path")

    def spawn_script_process(self):
        """
        Initializes for running an anonymous script
        sent from the BaseStation.

        Returns:
            obj:`Thread`: The thread that the script process
                ran on.
        """
        if self.p is not None and self.p.is_alive():
            print("Terminating spawned script process")
            self.p.exit()
        time.sleep(0.1)

        self.p = Thread(target=self.run_script)
        self.p.start()
        print("Starting thread!")

        # Return control to main after .1 seconds
        return self.p

    def spawn_named_script_process(self, script_name):
        """
        Initializes for running a pre-written, named script
        that already exists within the scripts directory on
        the current RPi.

        Args:
            script_name (obj:`str`): Name of the python file.
        Returns:
            obj:`Thread`: The thread that the script process
                ran on.
        """
        if self.p is not None and self.p.is_alive():
            print("Terminating spawned script process")
            self.p.exit()
        time.sleep(0.1)

        self.p = Thread(target=self.run_script_with_name, args=[script_name])
        self.p.start()

        # Return control to main after .1 seconds
        return self.p

    def run_script_with_name(self, script_name):
        """
        Responsible for actually executing the prewritten script.

        Args:
            script_name (obj:`str`): Name of the python file to run.
        """
        UserScript = importlib.import_module("scripts." + script_name)
        UserScript.run(self.bot)
        return None

    def run_script(self):
        """
        Responsible for actually executing the anonymous script.
        """
        print("Running the UserScript")
        from minibot.scripts import UserScript
        UserScript.run(self.bot)
        return None


def main():
    print("Initializing Minibot Software")
    CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())

    # Initialize bot and TCP.
    bot = Bot(config)
    tcp = TCP()
    print(tcp)

    # Initialize process.
    thread_udp = Thread(target=minibot.hardware.communication.UDP.udpBeacon)
    thread_udp.start()
    thread_udp.join()

    # Define MiniBot process.
    minibot_process = MiniBotProcess(bot)

    while True:
        tcpCmd = tcp.get_command()
        minibot_process.parse_command(tcpCmd)
        time.sleep(0.01)


def process_string(value):
    """
    Copy script sent from GUI into 'run' command
    So we can call that method to initiate the commands
    """
    cmds = value.splitlines()
    str = "def run(bot):\n"
    for i in range(len(cmds)):
        str += "    " + cmds[i] + "\n"
    return str


def process_payload(message):
    """
    Given a message/command sent through TCP, splits the
    message into the key and value.

    Args:
        message (obj:`str`): Command sent through TCP to parse.
    Returns:
        str, str: Key and value extracted from the command.
    """
    comma = message.find(",")
    start = message.find("<<<<")
    end = message.find(">>>>")

    return message[start + 4:comma], message[comma + 1:end]


if __name__ == "__main__":
    main()
