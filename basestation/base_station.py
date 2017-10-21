from basestation.bot.bot_manager import BotManager
from basestation.vision.vision_manager import VisionManager
from basestation.util.class_util import Singleton

# We define a metaclass for BaseStation - the BaseStation will be an instance
#  of the metaclass Singleton. This is very powerful as it reflects how the
# Singleton class describes how the instances will behave. In this case,
# the BaseStation will behave like a singleton.
# References:
# - https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python


class BaseStation(object, metaclass=Singleton):
    """
    Contains logic to manage and unify input and output between bots and vision
    sources. This class is a singleton to prevent accidental BaseStation
    duplication.
    """
    # https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

    def __init__(self):
        """
        Creates singleton base station. Contains a bot and vision manager.
        """
        self.bot_manager = BotManager()
        self.vision_manager = VisionManager()
        return

    def get_bot_manager(self):
        """
        Gets the bot manager associated with current BaseStation.
        """
        return self.bot_manager

    def get_vision_manager(self):
        """
        Gets the vision manager associated with current BaseStation.
        """
        return self.vision_manager
