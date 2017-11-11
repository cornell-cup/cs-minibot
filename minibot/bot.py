"""
Minibot object.
"""
import multiprocessing
from queue import Queue
from minibot.botstate import BotState
from minibot.hardware.rpi.gpio import DigitalInput, DigitalOutput, PWM, RGPIO
from minibot.peripherals.colorsensor import ColorSensor
from minibot.peripherals.hbridge import HBridge
import time

class Bot():
    """
    Minibot object class.
    Keeps track of the BotState (orientation, location, etc.) of the instance of MiniBot.
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

        # queue for extra unrecognized commands by parser
        self.extraCMD = Queue()

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
        self.motors.set_speed(0,0)

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
