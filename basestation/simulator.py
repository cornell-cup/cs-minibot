"""
Basestation Simulator
"""
class Simulator():

    def __init__(self):
        self.current_time = 0
        self.bots = []

    def add_bot(self, bot):
        self.bots.append(bot)

    def simulate(self, dt):
        self.current_time += dt
        for bot in self.bots:
            bot.simulate(dt)
