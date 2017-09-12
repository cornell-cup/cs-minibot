"""
Minibot GPIO classes.
"""

class PWM():
    """
    PWM used on a minibot.
    """
    def __init__(self, pin, frequency, duty_cycle=0):
        """
        Constructor.
        Args:
            pin (int): Pin that the PWM is connected to on the minibot.
            frequency (int): Frequency of the PWM.
            duty_cycle (int): Duty cycle of the PWM.
        """
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = duty_cycle

    def set_frequency(self, frequency):
        """
        Sets frequency of the PWM.
        """
        self.frequency = frequency

    def set_duty_cycle(self, duty_cycle):
        """
        Sets duty cycle of the PWM.
        """
        self.duty_cycle = duty_cycle

    def stop(self):
        """
        Stops the PWM.
        """
        pass
