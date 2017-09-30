"""
Bot manager.
"""

class BotManager:
    """
    Bot manager class.
    """
    def __init__(self):
        """
        Constructor.
        Initializes the UDP connection listener, creates an empty bot map, and starts
        the bot counter at zero.
        """
        self.bot_counter = 0
        self.bot_map = {}
        self.udp_connection = UDPConnection()

    def add_bot(self, bot):
        """
        Adds a bot to the bot manager list.
        Args:
            bot (:obj:`Bot`): Minibot object to add.
        """

        # TODO: Check if connection is active before doing the following.
        if True:
            bot_map[bot.get_name()] = bot
            return bot.get_name()
        else:
            raise Exception("The connection was not active. Not adding the bot.")
