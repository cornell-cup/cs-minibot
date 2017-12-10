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
import os

"""
    Loads UserScript file.
    Reloads file when it is run from GUI to reflect changes.
"""
US = importlib.import_module('minibot.scripts.UserScript')

CONFIG_LOCATION = '/home/pi/cs-minibot/minibot/configs/config.json'

p = None
def main():
    print("Initializing Minibot Software")
    p = None
    config_file = open(CONFIG_LOCATION)
    config = json.loads(config_file.read())
    bot = Bot(config)
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
        user_script_file = open("/home/pi/cs-minibot/minibot/scripts/UserScript.py",'w')
        val = process_string(value)
        user_script_file.write(val)
        user_script_file.close()
        p = spawn_script_process(p, bot)
    elif key == "RUN":
        filename = os.path.basename(value)
        filepath = "/home/pi/cs-minibot/minibot/scripts/" + filename
        print(filepath)
        if os.path.isfile(filepath):
            p = spawn_named_script_process(p, bot, filename.split('.')[0])
        else:
            print("Invalid File path")
    else:
        bot.extraCMD.put( (key, value) )

# Copy script sent from GUI into 'run' command
# So we can call that method to initiate the commands
def process_string(value):
    cmds = value.splitlines()
    str = "def run(bot):\n"
    for i in range(len(cmds)):
        str += "    " +cmds[i] + "\n"
    return str

def spawn_script_process(p, bot):
    time.sleep(0.1)
    p = Thread(target=run_script, args=[bot])
    p.start()
    return p
    
    # Return control to main after .1 seconds

def spawn_named_script_process(p,bot,script_name):
    time.sleep(0.1)
    p = Thread(target=run_script_with_name, args=[bot,script_name])
    p.start()
    # Return control to main after .1 seconds
    return p

def run_script_with_name(bot,script_name):
    UserScript = importlib.import_module("scripts." + script_name)
    UserScript.run(bot)

def run_script(bot):
    UserScript = importlib.reload(US)
    UserScript.run(bot)
    

if __name__ == "__main__":
    main()
