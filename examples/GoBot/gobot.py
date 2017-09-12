from minibot.bot import Bot
from minibot.hardware.rpi.gpio import PWM
from minibot.interface.servo import Servo

import math
import time

L_MOTOR_PIN = 12
R_MOTOR_PIN = 18

class GoBot(Bot):

    def __init__(self):
        Bot.__init__(self, "GoBot")
        self.l_motor = Servo(PWM(L_MOTOR_PIN, 2, 15))
        self.r_motor = Servo(PWM(R_MOTOR_PIN, 2, 15))
        self.l_motor.set(17)
        self.r_motor.set(13)

    def run(self):
        pass

if __name__ == "__main__":
    bot = GoBot()
    while True:
        bot.run()
