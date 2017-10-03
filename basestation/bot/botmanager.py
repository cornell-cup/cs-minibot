from __future__ import print_function
from basestation.bot.connection.udpconnection import UDPConnection as \
    UDPConnection
from basestation.bot.virtualbot.virtualbot import VirtualBot as VirtualBot

from typing import Optional

class BotManager:
    """
    Tracks and manages all virtual bots (vbots. Any vbot that you create a
    connection to should be tracked under this manager to prevent errors.
    VBots are uniquely identified by their names.
    """

    def __init__(self):
        """
        Initializes the UDP connection listener, creates an empty vbot map, and
        starts the vbot counter.
        """
        self.__vbot_counter = 0
        self.__vbot_map = {}
        self.__udp_connection = UDPConnection()
        self.__udp_connection.start()
        self.__vbot_exchange_map = {}

    def add_bot(self, vbot):
        """
        Adds a virtual bot to the virtual bot manager list.
        Args:
            vbot (VirtualBot): VirtualBot object to add.
        Returns:
            str: Name of the VirtualBot
        Raises:
            Exception: If the vbot connection is not active
        """
        if vbot.get_connection().is_connection_active():
            vbot_name = vbot.get_name()
            self.__vbot_map[vbot_name] = vbot
            return vbot_name
        else:
            raise Exception("The connection was not active. Not adding the bot.")

    def get_bot_by_name(self, name: str) -> Optional[VirtualBot]:
        return self.__vbot_map[name]

    def remove_bot_by_name(self, name: str) -> Optional[VirtualBot]:
        vbot = self.__vbot_map[name]
        del self.__vbot_map[name]
        return vbot