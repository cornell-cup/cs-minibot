"""
Minibot H-Bridge.
"""

class HBridge():
    """
    Minibot H-Bridge class.
    """
    def __init__(self, left_pin, left_pwm, right_pin, right_pwm):
        """
        Constructor.
        Args:
            left_pin (:obj:`DigitalOutput`): Left motor direction pin.
            left_pwm (:obj:`PWM`): PWM of the servo.
            right_pin (:obj:`DigitalOutput`): Right motor direction pin.
            right_pwm (:obj:`PWM`): PWM of the servo.
        """
        self.left_pin = left_pin
        self.left_pwm = left_pwm
        self.right_pin = right_pin
        self.right_pwm = right_pwm

        left_pwm.set_frequency(100)
        right_pwm.set_frequency(100)

    def set_speed(self, left, right):
        """
        Sets the speed of both motors.
        Args:
            left (float): The speed of the left motor (-1 to 1).
            right (float): The speed of the right motor (-1 to 1).
        """
        left = -max(min(left, 1.0), -1.0)
        right = -max(min(right, 1.0), -1.0)

        if left < 0:
            self.left_pin.set_high()
            self.left_pwm.set_duty_cycle(abs(left))
        else:
            self.left_pin.set_low()
            self.left_pwm.set_duty_cycle(1-abs(left))

        if right < 0:
            self.right_pin.set_high()
            self.right_pwm.set_duty_cycle(abs(right))
        else:
            self.right_pin.set_low()
            self.right_pwm.set_duty_cycle(1-abs(right))
