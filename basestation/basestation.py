"""
BaseStation for minibot.
"""

from minibot.basestation.bot.botmanager import BotManager as BotManager
from minibot.basestation.vision.visionmanager import VisionManager as VisionManager

class BaseStation():
    """
    Contains logic to manage and unify input and output between bots and vision sources.
    This class is a singleton to prevent accidental BaseStation duplication.
    """

    def __init__(self):
        """
        Constructor.
        Creates singleton base station. Contains a bot and vision manager.
        """
        self.bot_manager = BotManager()
        self.vision_manager = VisionManager()

    def get_station():
        """
        Gets the singleton instance of the currently active BaseStation.
        """
        if (instance != None):
            return instance
        else:
            instance = BaseStation()
            return instance

    def get_bot_manager():
        """
        Gets the bot manager associated with current BaseStation.
        """
        return self.bot_manager

    def get_vision_manager():
        """
        Gets the vision manager associated with current BaseStation.
        """
        return self.vision_manager
