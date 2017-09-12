from minibot.hardware.gpio import PWM as MPWM
import RPi.GPIO as RGPIO

RGPIO.setmode(RGPIO.BCM)

class PWM(MPWM):

    def __init__(self, pin, frequency, duty_cycle=0):
        MPWM.__init__(self, pin, frequency, duty_cycle)
        RGPIO.setup(pin, RGPIO.OUT)
        self.pwm = RGPIO.PWM(pin, frequency)
        self.pwm.start(duty_cycle)

    def set_frequency(self, frequency):
        MPWM.set_frequency(self, frequency)
        self.pwm.ChangeFrequency(frequency)

    def set_duty_cycle(self, duty_cycle):
        MPWM.set_duty_cycle(self, duty_cycle)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        MPWM.stop(self)
        self.pwm.stop()
