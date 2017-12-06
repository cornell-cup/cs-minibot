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
             loc_info {'x':, 'y':,'z':,'size':,'angle':,'type':}
        """
        #THIS NEEDS TO BE REDONE LATER
        if isinstance(loc_info, tuple):
            if bot_name not in self.locations: self.locations[bot_name] = {
                'size': 1,
                'type': 'bot',
                'angle':0
            }
            self.locations[bot_name]['x'] = loc_info[0]
            self.locations[bot_name]['y'] = loc_info[1]
            self.locations[bot_name]['z'] = loc_info[2]
        else:
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
        loc_data = self.locations[bot_name]
        return loc_data['x'], loc_data['y'], loc_data['z']

    def get_locations(self):
        """
        Returns list of all locations.
        NOTE: angle hardcoded to 0, size hardcoded to 1

        Returns:
            list of {'id':str, 'x':int, 'y':int, 'size':float, 'angle':int}
        """
        botlist = []
        for k in self.locations:
            v = self.locations[k]
            botlist.append({'id':k, 'x':v['x'], 'y':v['y'], 'size':v['size'], 'angle':v['angle']})
        return botlist
