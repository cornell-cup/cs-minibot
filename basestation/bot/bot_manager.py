from basestation.bot.connection.udp_connection import UDPConnection
from basestation.bot.virtualbot.virtual_bot import VirtualBot

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

    def add_bot(self, ip: str, port: int, vbot_name: str) -> Optional[str]:
        """
        Adds a virtual bot to the virtual bot manager list.

        Args:
            ip (str): The IP of the MiniBot
            port (int): The port of the MiniBot
            vbot_name (str): VirtualBot object to add.

        Returns:
            Optional[str]: Name of the VirtualBot or None

        Raises:
            Exception: If the vbot connection is not active
        """
        new_vbot = VirtualBot(ip, port, self.__safe_escape_name(vbot_name))

        if new_vbot.is_bot_connection_active():
            # vbot was successfully added; add it to the vbotmap and return
            # the vbot's name
            new_vbot_name = new_vbot.get_name()
            self.__vbot_map[new_vbot_name] = new_vbot
            return new_vbot.get_name()
        else:
            # bot was not added as the connection is not active; delete the
            # instance
            del new_vbot
            raise Exception("The connection was not active. Not adding the "
                            + "bot.")

    def get_bot_by_name(self, name: str) -> Optional[VirtualBot]:
        return self.__vbot_map.get(name, None)

    def remove_bot_by_name(self, name: str):
        vbot = self.__vbot_map.get(name, None)
        del self.__vbot_map[name]
        del vbot
        return

    def get_all_tracked_bots(self) -> list:
        """Returns a view of the vbots currently tracked"""
        return list(self.__vbot_map.values())

    def get_all_tracked_bots_names(self) -> list:
        """Returns a view of the names of the vbots currently tracked"""
        return list(self.__vbot_map.keys())

    def generate_bot_number(self) -> int:
        """Returns the next available (int) for a vbot number. Should not be
        used by anyone using the basestation. (?)"""
        self.__vbot_counter += 1
        return self.__vbot_counter

    def get_all_discovered_bots(self) -> list:
        """
        Returns a list of vbots' names which are detectable through UDP
        communication.
        """
        return list(self.__udp_connection.get_addresses())

    def get_bot_exchange(self, bot_id):
        """Returns the IP associated with vbot IP mapping"""
        return self.__vbot_exchange_map.get(bot_id, None)

    def set_bot_exchange(self, bot_id, bot_IP):
        """Adds an internal mapping from bot_id to bot_IP"""
        self.__vbot_exchange_map[bot_id] = bot_IP
        return

    def __safe_escape_name(self, name: str) -> str:
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
        if self.get_bot_by_name(name) is not None:
            name += str(self.generate_bot_number())
        return name
