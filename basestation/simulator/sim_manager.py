from basestation.bot.simbot.sim_bot import SimBot

class SimManager():
    """
    Tracks and manages all simulated bots
    """
    def __init__(self):
        #list of simbots
        self.__track_bots: []

    def add_bot(self, id: int, angle: int, x: int, y: int, size: int):
        """
        Adds a simbot to the list of tracked simbots
        Args:
            id (int): unique id of bot (should match index of list)
            angle (int): angle that bot is facing
            x (int): x-coordinate of bot
            y (int): y-coordinate of bot
            size (int): assuming square bot, length of one side of the bot
        """
        sim_bot = SimBot(id, angle, x, y, size)
        self.__track_bots.append(sim_bot)

    def update_direction(self, id: int, d: str):
        """
        Updates the simbot's coordinates based on input direction (f, b, l, r)

        Args:
            id (int): unique id of bot (should match index of list)
            d (str): 'f' (forward), 'b' (backward), 'l' (left), 'r' (right)
        Returns:
            SimBot object with updated coordinates
        """
        bot = self.__track_bots[id]
        if d == 'f':
            bot.set_y(bot.get_y + 1)
        elif d == 'b':
            bot.set_y(bot.get_y - 1)
        elif d == 'l':
            bot.set_x(bot.get_x - 1)
        else:
            bot.set_x(bot.get_x + 1)
        return bot




