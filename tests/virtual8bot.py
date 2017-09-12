from minibot.bot import Bot

import math
import time

class Virtual8Bot(Bot):
    is_simulatable = True
    figure8 = [
        ( 1.0, 1.0, 1.0),
        ( math.pi * 1.5, 0.0, 2.0),
        ( 2.0, 1.0, 1.0),
        ( math.pi * 1.5, 2.0, 0.0),
        ( 1.0, 1.0, 1.0),
    ]

    def __init__(self):
        Bot.__init__(self, "Virtual 8 Bot")
        self.l = 0
        self.r = 0
        self.t = 0
        self.state.radius = 1.0

    def set_motor(self, l, r):
        self.l = l
        self.r = r

    def update(self, dt):
        self.t += dt
        self.set_motor(0, 0)
        tt = 0
        for lt, l, r in self.figure8:
            tt += lt
            if self.t < tt:
                self.set_motor(l, r)
                break

    def simulate(self, dt):
        v = 0.5 * (self.r + self.l)
        w = 0.5 / self.state.radius * (self.r - self.l)
        self.state.angle += dt * w
        self.state.x += dt * v * math.cos(self.state.angle)
        self.state.y += dt * v * math.sin(self.state.angle)
