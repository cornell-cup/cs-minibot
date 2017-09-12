class Servo():

    def __init__(self, pwm):
        self.pwm = pwm

    def set(self, x):
        self.pwm.set_duty_cycle(x)
