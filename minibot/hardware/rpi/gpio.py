"""GPIO of the minibot, specific to the raspberry pi.
"""

from minibot.hardware.gpio import PWM as MPWM
import RPi.GPIO as RGPIO

# Sets mode of the GPIO.
RGPIO.setmode(RGPIO.BCM)

class PWM(MPWM):
    """
    Defines PWM used for a minibot. Inherits from MPWM.
    """
    def __init__(self, pin, frequency, duty_cycle=0):
        """Constructor.

        Args:
            pin (int): pin used for minibot.
            frequency (int):  frequency used for minibot's PWM.
            duty_cycle (int): duty cycle of minibot's PWM. Defaults to 0.
        """
        MPWM.__init__(self, pin, frequency, duty_cycle)
        RGPIO.setup(pin, RGPIO.OUT)
        self.pwm = RGPIO.PWM(pin, frequency)
        self.pwm.start(duty_cycle)

    def set_frequency(self, frequency):
        """Sets frequency of the PWM on the minibot.
        Args:
            frequency (int): New frequency on the minibot.
        """
        MPWM.set_frequency(self, frequency)
        self.pwm.ChangeFrequency(frequency)

    def set_duty_cycle(self, duty_cycle):
        """Sets duty cycle of the PWM on the minibot.
        Args:
            duty_cycle (int): New duty cycle for the PWM.
        """
        MPWM.set_duty_cycle(self, duty_cycle)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def stop(self):
        """Stops the PWM on the minibot.
        """
        MPWM.stop(self)
        self.pwm.stop()
