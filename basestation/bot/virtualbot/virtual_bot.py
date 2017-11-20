from basestation.bot.connection.tcp_connection import TCPConnection
from basestation.bot.sensors.sensor_center import SensorCenter
from basestation.bot.commands.command_center import CommandCenter
from basestation.util.exception_handling import *
import basestation.bot.bot_exchange as bot_exchange

import threading


class VirtualBot(object):
    """
    An instance of VirtualBot represents any MiniBot. We assume vbots may
    present information and receive information, so this is separated into
    the CommandCenter and SensorCenter. VirtualBots also have a persistent
    connection which is represented by Connection
    """

    def __init__(self, vbot_name: str, ip: str, port: int = 10000):
        """
        Sets up an instance of the VirtualBot using a TCP Connection.

        Args:
            vbot_name (str): The name of the MiniBot.
            ip (str): The IP of the MiniBot.
            port (int, optional): The port to establish the TCP connection on.
                Default=10000.
        """
        self.__tcp_connection = TCPConnection(ip, port=port)
        self.__name = vbot_name

        self.__command_center_obj = CommandCenter(self.__tcp_connection)
        self.__sensor_center_obj = SensorCenter()

        self.__tcp_listener_thread = self.TCPListener(self.__tcp_connection)
        self.__tcp_listener_thread.start()

        return

    def __del__(self):
        """
        Destructor for a VirtualBot object. Automatically called when
        destroying a VirtualBot object.

        Examples:
            `del <VirtualBot object>`
        """
        self.__tcp_connection.destroy()
        return

    def get_command_center(self) -> CommandCenter:
        """
        Returns:
             (CommandCenter): The Command Center associated with this
             VirtualBot.
        """
        return self.__command_center_obj

    def get_sensor_center(self) -> SensorCenter:
        """
        Returns:
             (SensorCenter): The Sensor Center associated with this VirtualBot.
        """
        return self.__sensor_center_obj

    def get_name(self) -> str:
        """
        Returns:
            (str): The name of this VirtualBot
        """
        return self.__name

    def is_bot_connection_active(self) -> bool:
        """
        Returns:
            (bool): True if the TCP connection associated with this
                VirtualBot is active. False otherwise
        """
        return self.__tcp_connection.is_connection_active()

    class TCPListener(threading.Thread):

        def __init__(self, t):
            """
            Create a TCPListener object using `t`'s TCP properties,
            and listens forever on a thread.

            Args:
                t (TCPConnection): Object of the TCP Connection to associate
                    this listener with.
            """
            super().__init__()
            self.tcp_connection_obj = t

        def run(self):
            """
            Run the TCP listener on a thread, parse and act on incoming
            information from the MiniBots.
            """
            try:
                while True:
                    if self.tcp_connection_obj.is_connection_active():
                        msg = self.tcp_connection_obj.receive()
                        print("Received message:\n", msg)
                        if msg is not None:
                            self.__tcp_parse_incoming(msg)

            except RuntimeError as e:
                msg = "TCP receive failed."
                log_exn_info(e, msg=msg)

        def __tcp_parse_incoming(self, data: str):
            """
            Breaks the data into key and value; calls
            `self.__tcp_act_on_incoming(...)` to act on the information
            received..

            Precondition: `data is not None`

            Args:
                data (str): A string to be parsed. Must start with* "<<<<" and
                    end with ">>>>". Key-value pair should be separated by ":"
            """
            print("Receiving incoming TCP!")
            print("Message: " + data)
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
            Acts based on key and value, MiniBot sending information should send
            key and value, MiniBot requesting information should only send key.

            Args:
                key (str): An instruction to be executed.
                value (str): Should qualify the `key`.
            """
            if len(value) != 0:
                # MiniBot requesting information
                value_to_send = bot_exchange.msg_map.get(key, None)
                self.tcp_connection_obj.sendKV(key, value_to_send)
            else:
                # MiniBot sending information
                bot_exchange.msg_map[key] = value

            return
