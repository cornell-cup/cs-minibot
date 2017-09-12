from minibot.botstate import BotState

class Bot():

    def __init__(self, name):
        self.name = name
        self.state = BotState()

    def get_state(self):
        return self.state

    def run(self):
        raise NotImplementedError("Bot.update not implemented")
