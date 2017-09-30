from minibot.botstate import BotState
from minibot.peripherals.sensors.Sensor import Sensor
from minibot.peripherals.actuators.Actuator import Actuator

class Bot(object):

    def __init__(self, name):
        self.name = name
        self.state = BotState()
        self.sensors = {}
        self.actuators = {}

    def get_state(self):
        return self.state

    def add_sensor(self, name):
        if name in self.sensors:
            print "Sensor already exists"
            return

        sensor = Sensor(self, name)
        self.sensors[name] = sensor

    def add_actuator(self, name):
        if name in self.actuators:
            print "Actuator already exists"
            return

        actuator = Actuator(self, name)
        self.actuators[name] = actuator

    def get_sensor(self, name):
        if name in self.sensors:
            return self.sensors[name]
        return None

    def get_sensors(self):
        return self.sensors.values()

    def get_actuator(self, name):
        if name in self.actuators:
            return self.actuators[name]
        return None

    def get_actuators(self):
        return self.actuators.values()

    def run(self):
        raise NotImplementedError("Bot.update not implemented")
