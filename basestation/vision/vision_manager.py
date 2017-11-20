"""
Vision manager.
"""


class VisionManager:
    """
    Keeps track of vision components
    """
    def __init__(self):
        # Map of bot name and its location.
        self.locations = {}
        # How many bots are registered via vision system.
        self.counter = 0

    def update_location(self, bot_name, loc_info):
        """
        Updates the location of a given bot with the location information.

        Args:
             bot_name (obj:`str`): Name of the bot.
             loc_info (int, int, int): X, Y, and Z coordinates of the bot.
        """
        self.locations[bot_name] = loc_info
        return self.locations

    def get_location(self, bot_name):
        """
        Returns location information of the given bot.

        Args:
            bot_name (obj:`str`): Name of the bot.
        Returns:
            (int, int, int): X, Y, and Z coordinates of the bot.
        """
        return self.locations[bot_name]
