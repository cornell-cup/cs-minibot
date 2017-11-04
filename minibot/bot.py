"""
Minibot object.
"""
import multiprocessing
from multiprocessing import Queue
from minibot.botstate import BotState
from minibot.hardware.rpi.gpio import DigitalInput, DigitalOutput, PWM, RGPIO
from minibot.peripherals.colorsensor import ColorSensor
from minibot.peripherals.hbridge import HBridge

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

    def run(self):
        """
        Runs the minibot.
        """
        self.motors.set_speed(0, 0)
