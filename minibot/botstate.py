"""
BotState object.
"""

class BotState():
    """
    BotState class.
    Keeps track of the current state of the minibot.
    """
    x = 0
    y = 0
    angle = 0
    radius = 0

    def __init__(self, x=0, y=0, angle=0, radius=0):
        """
        Constructor for BotState. Assumes bot begins at origin with no orientation offset.
        Note:
            All parameters default to 0.
        Args:
            x (int): X coordinate of the bot.
            y (int): Y coordinate of the bot.
            angle (int): Angle orientation of robot from the horizontal (x-axis).
            radius (int): Radius of minibot.
        """
        self.x = x
        self.y = y
        self.angle = angle
        self.radius = radius
