"""
Minibot object.
"""
import Queue

from minibot.botstate import BotState
from minibot.hardware.rpi.gpio import DigitalInput, DigitalOutput, RGPIO
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

        self._parse_config(config)

    def _parse_config(self, config):
        """
        Parses config dictionary and registers peripherals.
        Args:
             config (dict): Dictionary of config information.
        """
        for actuator in config["actuators"]:
            if actuator["type"] == "GpioMotor":
                name = actuator["name"]
                pinPWM = actuator["pinPWM"]
                pinHighLow = actuator["pinHighLow"]
                reversed = actuator["reversed"]
                DigitalOutput(self, name, pinPWM, pinHighLow, reversed, RGPIO)
            elif actuator["type"] == "I2CMotor":
                name = actuator["name"]
                address = actuator["address"]
                number = actuator["number"]
                reversed = actuator["reversed"]
                DigitalOutput(self, name, address, number, reversed)
            else:
                print("ERROR: Unknown actuator in config")

        for sensor in config["sensors"]:
            if sensor["type"] == "ColorSensor":
                name = sensor["name"]
                pin = sensor["pin"]
                ColorSensor(self, name, pin)
            else:
                print("ERROR: Unknown sensor in config")

        # queue for extra unrecognized commands by parser
        self.extraCMD = Queue()
        # TODO: Sensor parsing

        # Meta actuator. TODO: Make configurable
        self.left_motor = self.actuators["leftMotor"]
        self.right_motor = self.actuators["rightMotor"]
        self.two_wheel_movement = HBridge(self, "two_wheel_movement",\
                                          self.left_motor, self.right_motor)

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
        raise NotImplementedError("Bot.run not implemented")
