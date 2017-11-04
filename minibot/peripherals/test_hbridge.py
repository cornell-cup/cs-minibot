"""
Test for hbridge
"""
import unittest
import minibot.hardware.virtual_gpio.gpio import DigitalOutput, PWM
from minibot.peripherals.hbridge import HBridge

class TestHBridge(unittest.TestCase):
    """
    Tests to makes sure movements work correctly
    """

    def test_initially_stopped(self):
        """ Test bot is in stopped state """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        self.assertEqual(hbridge.left_pin.state, 0)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 100)
        self.assertEqual(hbridge.right_pin, 0)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 100)

    def test_forward(self):
        """ Tests to make sure moves forward correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(1, 1)


if __name__ == "__main__":
    unittest.main()
