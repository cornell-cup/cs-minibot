from basestation.bot.connection.udp_connection import UDPConnection
from basestation.bot.virtualbot.virtual_bot import VirtualBot
from basestation.bot.simbot.sim_bot import SimBot

from typing import Optional
from os import listdir
from os.path import isfile, join
from random import *


class BotManager(object):
    """
    Tracks and manages all virtual bots (bots. Any bot that you create a
    connection to should be tracked under this manager to prevent errors.
    Bots are uniquely identified by their names.
    """

    def __init__(self):
        """
        Initializes the UDP connection listener, creates an empty bot map, and
        starts the bot counter.
        """
        self.__bot_counter = 0
        self.__bot_map = {}
        self.__udp_connection = UDPConnection()
        self.__udp_connection.start()
        #This is for fun. Changed to either unique ID generator or to user custom name
        self.__sim_names = ["leo", "jesse", "ashley", "lesley", "celine", "danny", "heather", "lauren", "chelsea", "jimmy", "han",
                 "trevor", "matt li", "james", "danny mf yang", "fire lord", "kevin", "anmol", "scott 'the cornell cup' wu"]
        return

    def add_bot(self, bot_name: str, ip: str, port: int = 10000) -> Optional[str]:

        """

        Adds a virtual bot to the virtual bot manager list.

        Args:
            bot_name (str): MiniBot's name.
            ip (str): The IP of the MiniBot.
            port (int, optional): The port of the MiniBot's TCP Connection.
                Default = 10000

        Returns:
            Optional[str]: Name of the VirtualBot object created, emulating
                the MiniBot.

        Raises:
            Exception: Raised if the TCP connection was or went inactive
                while creating the VirtualBot object.
        """
        if type == "minibot":
            new_vbot = VirtualBot(self.__safe_escape_name(bot_name), ip, port=port)

            if new_vbot.is_bot_connection_active():
                new_vbot_name = new_vbot.get_name()
                self.__bot_map[new_vbot_name] = new_vbot
                return new_vbot.get_name()
            else:
                del new_vbot
                raise Exception("The connection was not active. Not adding the "
                                + "bot.")

    def add_simbot(self, id: int, angle: int, x: int, y: int, size: int):
        """
        Adds a simbot to the list of tracked simbots
        Args:
            id (int): unique id of bot (should match index of list)
            angle (int): angle that bot is facing
            x (int): x-coordinate of bot
            y (int): y-coordinate of bot
            size (int): assuming square bot, length of one side of the bot
        """
        name = self.__sim_names[randint(0, len(self.__sim_names))]
        sim_bot = SimBot(id, angle, x, y, size)
        print(sim_bot)
        self.__bot_map[name] = sim_bot
        return name


    def get_bot_by_name(self, name: str) -> Optional[VirtualBot]:
        """
        Returns the VirtualBot, which has the name `name`. If no VirtualBot
        `v` exists such that `v.get_name() == name` then `None` is
        returned.

        Args:
            name (str): The name of the MiniBot.
        """
        return self.__bot_map.get(name, None)

    def remove_bot_by_name(self, name: str):
        """
        Remove the VirtualBot `v` which has the `v.get_name() == name`.
        If no such VirtualBot exists, then no operation is done.

        Args:
            name (str): The name of the MiniBot.

        Returns:
            (bool): True if VirtualBot successfully removed, False if
                operation failed.
        """
        bot = self.__bot_map.get(name, None)

        try:
            del self.__bot_map[name]
        except KeyError:
            return False

        if bot is not None:
            del bot
            return True
        else:
            return False

    def get_all_tracked_bots(self) -> list:
        """
        Returns a list of VirtualBots currently tracked.
        """
        return list(self.__bot_map.values())

    def get_all_tracked_bots_names(self) -> list:
        """
        Returns a list of the names of VirtualBots currently tracked.
        """
        return list(self.__bot_map.keys())

    def get_all_discovered_bots(self) -> list:
        """
        Returns a list of the names of VirtualBots, which are detectable
        through UDP broadcast.
        """
        return list(self.__udp_connection.get_addresses())

    def get_minibot_scripts(self):
        """
        Returns a list of the scripts avaliable on the minibot.
        """
        path = "./minibot/scripts"
        files = [f for f in listdir(path) if isfile(join(path, f))]
        return files

    def __generate_bot_number(self) -> int:
        """
        Returns the next available `int` to be added to the name of the
        VirtualBot v, if there exists a Virtual Bot v2 such that
        `v.get_name() == v2.get_name()`.
        """
        # todo: not sure if this works as intended
        # possible problem: Let's say these bots exist: bot, bot0, testbot,
        # and we want to add testbot to the list. I have a hunch that it will be
        # added as testbot1 instead of testbot0.
        self.__bot_counter += 1
        return self.__bot_counter

    def __safe_escape_name(self, name: str) -> str:
        """
        Safely escapes the name of the bot to ensure it is unique and
        returns that string. This has a simple implementation for now,
        but could be extended to guarantee uniqueness. For anyone using a
        MiniBot, this means names should only used [a-zA-Z] characters.

        Args:
            name (str): The name to be escaped.

        Returns:
            (str) The safely escaped name.
        """
        if self.get_bot_by_name(name) is not None:
            name += str(self.__generate_bot_number())
        return name
