from basestation.bot.connection.tcp_connection import TCPConnection
from basestation.bot.sensors.sensor_center import SensorCenter
from basestation.bot.commands.command_center import CommandCenter
from basestation.util.exception_handling import *
import basestation.bot.bot_exchange as bot_exchange

import threading
from typing import Optional


class VirtualBot(object):
    """
    An instance of VirtualBot represents any MiniBot. We assume vbots may
    present information and receive information, so this is separated into
    the CommandCenter and SensorCenter. Vbots also have a persistent
    connection which is represented by Connection
    """

    def __init__(self, ip: str, port: int, vbot_name: str):
        """
        Set up an instance of the VirtualBot using a TCP Connection
        Args:
            tcp_connection_obj (TCPConnection): A TCP Connection that has
            already been created
        """
        self.__tcp_connection = TCPConnection(ip, port)
        self.__name = vbot_name

        self.__command_center_obj = CommandCenter(self.__tcp_connection)
        self.__sensor_center_obj = SensorCenter()

        self.__tcp_listener_thread = self.TCPListener(self.__tcp_connection)
        self.__tcp_listener_thread.start()

        return

    def __del__(self):
        self.__tcp_connection.destroy()
        print(self.__name + " is dead.")
        return

    def get_command_center(self) -> CommandCenter:
        return self.__command_center_obj

    def get_sensor_center(self) -> SensorCenter:
        return self.__sensor_center_obj

    def get_name(self) -> str:
        return self.__name

    def is_bot_connection_active(self) -> bool:
        return self.__tcp_connection.is_connection_active()

    class TCPListener(threading.Thread):

        def __init__(self, t):
            super().__init__()
            self.tcp_connection_obj = t

        def run(self):
            try:
                while True:
                    if self.tcp_connection_obj.is_connection_active():
                        msg = self.tcp_connection_obj.receive()
                        if msg is not None:
                            self.__tcp_parse_incoming(msg)

            except RuntimeError as e:
                msg = "TCP receive failed."
                log_exn_info(e, msg=msg)

        def __tcp_parse_incoming(self, data: Optional[str]):
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
                    self.__tcp_act_on_incoming(key, value)

            return

        def __tcp_act_on_incoming(self, key: str, value: str):
            """
            Acts based on key and value, bot sending information should send
            key and value, bot requesting information should only send key

            Args:
                key (str): An instruction to be executed
                value (str): Should qualify the instruction
            """
            if len(value) != 0:
                # MiniBot requesting information
                value_to_send = bot_exchange.msg_map.get(key, None)
                self.tcp_connection_obj.sendKV(key, value_to_send)
            else:
                # MiniBot sending information
                bot_exchange.msg_map[key] = value

            return
