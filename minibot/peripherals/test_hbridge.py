"""
Test for hbridge
"""
import unittest
from minibot.hardware.virtual_gpio.gpio import DigitalOutput, PWM
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
        hbridge.set_speed(0,0)
        self.assertEqual(hbridge.left_pin.state, 0)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 1)
        self.assertEqual(hbridge.right_pin.state, 0)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 1)

    def test_forward(self):
        """ Tests to make sure moves forward correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(1, 1)
        self.assertEqual(hbridge.left_pin.state, 0)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 0)
        self.assertEqual(hbridge.right_pin.state, 0)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 0)

    def test_backward(self):
        """ Tests to make sure moves backward correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(-1, -1)
        self.assertEqual(hbridge.left_pin.state, 1)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 1)
        self.assertEqual(hbridge.right_pin.state, 1)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 1)

    def test_counterclockwise(self):
        """ Tests to make sure turns left correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(-1, 1)
        self.assertEqual(hbridge.left_pin.state, 1)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 1)
        self.assertEqual(hbridge.right_pin.state, 0)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 0)

    def test_clockwise(self):
        """ Tests to make sure turns left correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(1, -1)
        self.assertEqual(hbridge.left_pin.state, 0)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 0)
        self.assertEqual(hbridge.right_pin.state, 1)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 1)

    def test_pivotright(self):
        """ Tests to make sure turns right correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(1, 0)
        self.assertEqual(hbridge.left_pin.state, 0)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 0)
        self.assertEqual(hbridge.right_pin.state, 0)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 1)

    def test_pivotleft(self):
        """ Tests to make sure turns left correctly """
        hbridge = HBridge(DigitalOutput(10),
                          PWM(13),
                          DigitalOutput(24),
                          PWM(18))
        hbridge.set_speed(0, 1)
        self.assertEqual(hbridge.left_pin.state, 0)
        self.assertEqual(hbridge.left_pwm.duty_cycle, 1)
        self.assertEqual(hbridge.right_pin.state, 0)
        self.assertEqual(hbridge.right_pwm.duty_cycle, 0)

if __name__ == "__main__":
    unittest.main()
