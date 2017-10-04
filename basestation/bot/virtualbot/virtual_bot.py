from basestation.base_station import BaseStation as BaseStation
from basestation.bot.connection.tcp_connection import TCPConnection as \
    TCPConnection
from basestation.bot.sensors.sensor_center import SensorCenter as SensorCenter


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
        self.__command_center_obj = CommandCenter(tcp_connection_obj)
        self.__sensor_center_obj = SensorCenter()
        # todo: start the tcp_listener_thread
        # todo: add the name of the vbot

    def get_command_center(self):
        return self.__command_center_obj

    def get_sensor_center(self):
        return self.__sensor_center_obj

    # todo: implement the inner class TCPListenerThread
