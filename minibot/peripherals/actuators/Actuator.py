import logging

# Abstract class representing an actuator
class Actuator(object):
    def __init__(self, bot, name):
        self.name = name
        logging.info("Actuator being registered: " + str(self.name))

    def read(self):
        logging.warn("Invalid: Abstract Class")

    def set(self, value):
        logging.warn("Invalid: Abstract Class")

    def get_name(self):
        return self.name
