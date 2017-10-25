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

    tcpInstance = TCP()
    print(tcpInstance)
    thread_udp = Thread(target= minibot.hardware.communication.UDP.udpBeacon)
    thread_udp.start()    
    while True:
        tcpCmd = tcpInstance.get_command()

def parse_command(cmd, bot, p):
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
            bot.get_actuator_by_name("two_wheel_movement").move(int(float(values[0])),
                                                                int(float(values[1])))
        except Exception as e:
            print(e)
            print("oh no!")
            pass
    elif key == "SCRIPT":
        user_script_file = open("scripts/sample.py", 'w')
        user_script_file.write(value)
        user_script_file.close()
        p = spawn_script(p, bot, None)
        return p
    elif key == "RUN":
        p = spawn_script(p, bot, value)
    else:
        bot.extraCMD.put((key, value))
        print("Unknown key: " + key)
        print("Cmd: " + cmd)
    return None

def spawn_script(p, bot, value):
    """
    Initializes
    """
    if (p and p.is_alive()):
        p.terminate()
    time.sleep(0.1)

    p = Thread(target=run_script, args=[bot, value])
    p.start()
    return p

def run_script(bot, name):
    """
    Runs a script on the bot.

    Args:
         bot (:obj:`Bot`): MiniBot object to run the script on.
         name (:obj:`str`): Name of bot. Optional. If None, runs user_script.py
    """
    if name:
        sys.path.insert(0, './lib')
        UserScript = importlib.import_module("scripts." + script_name)
    else:
        from minibot.scripts import user_script as UserScript

    UserScript.run(bot)


if __name__ == "__main__":
    main()
