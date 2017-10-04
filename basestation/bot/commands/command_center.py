from basestation.bot.virtualbot.virtual_bot import VirtualBot
from basestation.bot.connection.tcp_connection import TCPConnection
from basestation.bot.commands.four_wheel_movement import FourWheelMovement

import json


class CommandCenter(FourWheelMovement):
    """
    An instance whose methods are all the commands that can be issued to a vbot.
    Each VirtualBot must implement this class with their own commands.
    """

    def __init__(self, connection_obj):
        self.__connection = connection_obj
        self.__record = False

    def toggle_logging(self):
        self.__record = True

    def is_logging(self):
        return self.__record

    def sendKV(self, key, value):
        return self.__connection.sendKV(key, value)

    def get_all_data(self):
        # todo: not implemented yet
        return None

    def set_wheel_power(self, fl, fr, bl, br):
        return self.__sendKV("WHEELS", str(fl) + "," + str(fr) + "," + str(
            bl) + "," + br)

    def get_connection(self):
        return self.__connection