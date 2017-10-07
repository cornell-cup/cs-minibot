from basestation.bot.connection.udp_connection import UDPConnection as \
    UDPConnection
from basestation.bot.virtualbot.virtual_bot import VirtualBot as VirtualBot

from typing import Optional


class BotManager(object):
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
        return

    def add_bot(self, vbot: VirtualBot) -> Optional[str]:
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
            return None

    def get_bot_by_name(self, name: str) -> Optional[VirtualBot]:
        return self.__vbot_map[name]

    def remove_bot_by_name(self, name: str) -> Optional[VirtualBot]:
        vbot = self.__vbot_map[name]
        del self.__vbot_map[name]
        return vbot

    def get_all_tracked_bots(self):
        """Returns a view of the vbots currently tracked"""
        return self.__vbot_map.values()

    def get_all_tracked_bots_names(self):
        """Returns a view of the names of the vbots currently tracked"""
        return self.__vbot_map.keys()

    def generate_bot_number(self):
        """Returns the next available (int) for a vbot number. Should not be
        used by anyone using the basestation. (?)"""
        self.__vbot_counter += 1
        return self.__vbot_counter

    def get_all_discovered_bots(self):
        """
        Returns a set of vbots which are detectable through UDP
        communication.
        """
        return self.__udp_connection.get_address_set()

    def get_bot_exchange(self, bot_id):
        """Returns the IP associated with vbot IP mapping"""
        return self.__vbot_exchange_map[bot_id]

    def set_bot_exchange(self, bot_id, bot_IP):
        """Adds an internal mapping from bot_id to bot_IP"""
        self.__vbot_exchange_map[bot_id] = bot_IP
        return
