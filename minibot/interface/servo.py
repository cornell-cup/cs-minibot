"""
Minibot Servos.
"""

class Servo():
    """
    Minibot Servo class.
    """
    def __init__(self, pwm):
        """Constructor.
        Args:
            pwm (:obj:`PWM`): PWM of the servo.
        """
        self.pwm = pwm

    def set(self, duty_cycle):
        """Sets duty cycle of a servo's PWM.
        Args:
            duty_cycle (int): Duty cycle of PWM to set.
        """
        self.pwm.set_duty_cycle(duty_cycle)
