import unittest

from basestation.simulator import Simulator
from tests.virtual8bot import Virtual8Bot

import math

def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))

class TestVirtual8BotPhysics(unittest.TestCase):

    def test_simulation(self):
        sim = Simulator()
        bot = Virtual8Bot()

        sim.add_bot(bot)
        m = 1.0 + math.sqrt(2) / 2.0
        checkpoints = [
            ( 0,    0),
            ( 1,    0),
            ( m,    m),
            ( 0,    1),
            ( 0,    0),
            ( 0, -1),
            (-m, -m),
            (-1,    0),
            ( 0,    0),
        ]
        threshold = 0.1
        next_checkpoint = 0
        t = 0
        dt = 0.01

        while next_checkpoint < len(checkpoints) and t < 15:
            sim.simulate(dt)
            bot.update(dt)
            t += dt
            state = bot.get_state()
            cx, cy = checkpoints[next_checkpoint]
            if dist(cx, cy, state.x, state.y) < threshold:
                next_checkpoint += 1

        self.assertEqual(next_checkpoint, len(checkpoints))

if __name__=="__main__":
    unittest.main()
