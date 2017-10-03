import logging

# Abstract class representing a sensor
class Sensor(object):
    def __init__(self, bot, name):
        self.name = name
        print "Sensor being registered: " + str(self.name)

    def read(self):
        logging.warn("Invalid: Abstract Sensor Class Reading")

    def get_name(self):
        return self.name