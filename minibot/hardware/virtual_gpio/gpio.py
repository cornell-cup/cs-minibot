"""
Fake class to help with testing GPIO without a physical bot (used to simulate gpio)
"""

class DigitalInput():
    """
    Digital input pin.
    """
    def __init__(self, pin):
        """
        Constructor.
        Args:
            pin (int): Digital pin number.
        """
        self.pin = pin

    def read(self):
        """
        Read input from the digital pin.
        Return:
            int: 0 or 1 for LOW or HIGH voltage.
        """
        return 0

class DigitalOutput():
    """
    Digital output pin.
    """

    def __init__(self, pin):
        """
        Constructor.
        Args:
            pin (int): Digital pin number.
        """
        self.pin = pin
        self.state = 0

    def set_low(self):
        """
        Set the digital output pin to low.
        """
        self.state = 0

    def set_high(self):
        """
        Set the digital output pin to high.
        """
        self.state = 1

class PWM():
    """
    PWM used on a minibot.
    """
    def __init__(self, pin, frequency=1, duty_cycle=0):
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
        self.started = False

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
        self.started = False

    def start(self):
        """
        Starts the PWM.
        """
        self.started = True
