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
        pass
