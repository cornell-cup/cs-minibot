"""
Minibot object. Tied to the Raspberry Pi, and separate from the
virtual minibot used on the GUI side.
"""

import json
import multiprocessing
from multiprocessing import Queue
import RPi.GPIO as RGPIO

from minibot.botstate import BotState
from minibot.hardware.rpi.gpio import DigitalInput, DigitalOutput, PWM
from minibot.peripherals.colorsensor import ColorSensor
from minibot.peripherals.hbridge import HBridge
import time

class Bot():
    """
    Minibot object class.
    Keeps track of the BotState (orientation, location, etc.) of the instance of MiniBot.
    Interface between software and hardware.
    """
    def __init__(self, config):
        """
        Constructor for minibot.
        Args:
            config (dict): Dictionary of config information for bot hardware.
        """
        self.name = config['name']
        self.state = BotState()
        self.sensors = {}
        self.actuators = {}
        self.motors = None
        self._parse_config(config)

    def _parse_config(self, config):
        """
        Parses config dictionary and registers peripherals.
        Args:
             config (dict): Dictionary of config information.
        """
        self.actuators["left"] = config["actuators"][0]
        self.actuators["right"] = config["actuators"][1]
        self.motors = HBridge(DigitalOutput(self.actuators["left"]["pinHighLow"]),
                      PWM(self.actuators["left"]["pinPWM"]),
                      DigitalOutput(self.actuators["right"]["pinHighLow"]),
                      PWM(self.actuators["right"]["pinPWM"]))

    def get_state(self):
        """
        Gets the BotState of the minibot.
        Returns:
            BotState of the minibot.
        """
        return self.state

    def stop(self):
        """
        Moves the bot forward at a percentage of its full power
        :param power The percentage of the bot's power to use from 0-100
        :return True if the action is supported
        """
        self.motors.set_speed(0, 0)

    def parse_command(self, cmd, tcp):
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
                self.motors.set_speed(int(values[0]) / 100., int(values[1]) / 100.)
            except Exception as e:
                print(e)
                print("oh no!")
                pass
        elif key == "REQUEST":
            try:
                values = value.split(",")
                self.send_data(values[0], tcp)
            except Exception as e:
                print(e)
                print("Failed!")
                pass

    def send_data(self, type, tcp):
        """
        Sends bot data to basestation.
        Args:
            type (str): Type of data that is being requested of the bot.
            tcp (obj:`TCP`): TCP instance of the connection between bot and
                             BaseStation.
        """
        if not tcp or not type:
            print("TCP connection or TYPE not recognized.")
        elif type == "SENSORS":
            data = {}
            for sensor_name in self.sensors:
                data[sensor_name] = self.sensors[sensor_name].read()
            final_data = json.dumps(data)
            print("Sending sensor data to BaseStation: " + final_data)
            tcp.send_to_basestation(type, final_data)

    def move_forward(self, power):
        """
        Moves the bot forward at a percentage of its full power
        :param power The percentage of the bot's power to use from 0-100
        :return True if the action is supported
        """
        self.motors.set_speed(power/100,power/100)

    def move_backward(self, power):
        """
        Moves the bot backward at a percentage of its full power
        :param power The percentage of the bot's power to use from 0-100
        :return True if the action is supported
        """
        self.motors.set_speed(-power/100,-power/100)

    def turn_clockwise(self, power):
        """
        Moves the bot clockwise  at a percentage of its full power
        :param power The percentage of the bot's power to use from 0-100
        :return True if the action is supported
        """
        self.motors.set_speed(power/100,-power/100)

    def turn_counter_clockwise(self, power):
        """
        Moves the bot counter-clockwise at a percentage of its full power
        :param power The percentage of the bot's power to use from 0-100
        :return True if the action is supported
        """
        self.motors.set_speed(-power/100,power/100)

    def set_wheel_power(self, left, right):
        """
        Sets the power of the bot's wheels as a percentage from -100 to 100. If a wheel
        specified does not exist, the power for that wheel is ignored.
        :param front_left power to deliver to the front_left wheel
        :param front_right power to deliver to the front_right wheel
        :param back_left power to deliver to the back_left wheel
        :param back_right power to deliver to the back_right wheel
        :return True if the action is supported
        """
        self.motors.set_speed(left/100,right/100)

    def wait(self, t):
        """
        Waits for a duration in seconds.
        :param t The duration in seconds
        """
        time.sleep(t)

    def register_actuator(self,actuator):
        self.actuators[actuator.name] = actuator

    def get_actuator_by_name(self, name):
        return self.actuators[name]

    def get_all_actuators(self):
        return self.actuators.values()
