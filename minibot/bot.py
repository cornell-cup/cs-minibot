"""
Minibot object.
"""

from minibot.botstate import BotState

class Bot():
    """
    Minibot object class.
    Keeps track of the BotState (orientation, location, etc.) of the instance of MiniBot.
    """
    def __init__(self, name):
        """
        Constructor for minibot.
        Args:
            name (:obj:`str`): Name of minibot.
            state (:obj:`BotState`): BotState of the minibot.
        """
        self.name = name
        self.state = BotState()
        self.sensors = {}
        self.actuators = {}

    def get_state(self):
        """
        Gets the BotState of the minibot.
        Returns:
            BotState of the minibot.
        """
        return self.state

    def run(self):
        """
        Runs the minibot.
        """
        raise NotImplementedError("Bot.run not implemented")
