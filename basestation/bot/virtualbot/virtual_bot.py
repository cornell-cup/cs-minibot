from basestation.base_station import BaseStation as BaseStation
from basestation.bot.connection.tcp_connection import TCPConnection
from basestation.bot.sensors.sensor_center import SensorCenter
from basestation.bot.commands.command_center import CommandCenter

import threading
import logging
import sys


class VirtualBot(object):
    """
    An instance of VirtualBot represents any MiniBot. We assume vbots may
    present information and receive information, so this is separated into
    the CommandCenter and SensorCenter. Vbots also have a persistent
    connection which is represented by Connection
    """

    def __init__(self, tcp_connection_obj, vbot_name):
        """
        Set up an instance of the VirtualBot using a TCP Connection
        Args:
            tcp_connection_obj (TCPConnection): A TCP Connection that has
            already been created
        """
        self.__connection = tcp_connection_obj
        self.__name = self.__safe_escape_name(vbot_name)

        self.__command_center_obj = CommandCenter(tcp_connection_obj)
        self.__sensor_center_obj = SensorCenter()
        # todo: start the tcp_listener_thread

    def get_command_center(self):
        return self.__command_center_obj

    def get_sensor_center(self):
        return self.__sensor_center_obj

    def get_name(self):
        return self.__name

    def get_connection(self):
        return self.__connection

    @staticmethod
    def __safe_escape_name(name):
        """
        Safely escapes the name of the vbot to ensure it is unique and
        returns that string. This has a simple implementation for now,
        but could be extended to guarantee uniqueness. For anyone using a
        MiniBot, this means names should only used [a-zA-Z] characters.

        Args:
            name (str): The name to be escaped

        Returns:
            (str) The safely escaped name
        """
        bot_manager_obj = BaseStation().get_bot_manager()
        if bot_manager_obj.get_bot_by_name(name).is_present():
            name += str(bot_manager_obj.generate_bot_number())
        return name

    class TCPListenerThread(threading.Thread):
        
        def __init__(self, t, group=None, target=None, name=None, args=(),
                     kwargs=None):
            super().__init__(group=group, target=target, name=name, args=args,
                             kwargs=kwargs)
            self.__tcp_connection = t
            return
            
        def run(self):
            try:
                while True:
                    if self.__tcp_connection.is_active():
                        message = self.__tcp_connection.receive()
                        if message is not None:
                            self.__parse_incoming(message)
            except RuntimeError as e:
                logging.debug("TCP receive failed.")
                # print traceback
                tb = sys.exc_info()[2]
                e.with_traceback(tb)

        def __parse_incoming(self, data):
            """
            Breaks the data into key and value
            Precondition: data != None

            Args:
                data (str): A string to be parsed. Must start with "<<<<" and
                    end with ">>>>". Key-value pair should be separated by ":"
            """
            if data is not None:
                start = data.index("<<<<")
                comma = data.index(",")
                end = data.index(">>>>")
                if start != -1 and comma != -1 and end != -1:
                    key = data[start + 4:comma]
                    value = data[comma + 1:end]
                    self.__act_on_incoming(key, value)

        def __act_on_incoming(self, key, value):
            """
            Acts based on key and value, bot sending information should send
            key and value, bot requesting information should only send key

            Args:
                key (str): An instruction to be executed
                value (str): Should qualify the instruction
            """
            bot_manager_obj = BaseStation().get_bot_manager()
            if len(value) != 0:
                # MiniBot requesting information
                value_to_send = bot_manager_obj.get_bot_exchange(key)
                self.__tcp_connection.sendKV(key, value_to_send)
            else:
                # MiniBot sending information
                bot_manager_obj.set_bot_exchange(key, value)
