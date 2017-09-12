"""
Unit tests for minibot.
"""

import unittest

from minibot.botstate import BotState

class TestBotBasics(unittest.TestCase):
    """
    Tests basic functionalities of the minibot, such as movement and bot states.
    """
    def test_default_state(self):
        """
        Tests the default state, i.e. whether upon creating a minibot, the bot is detected to
        begin at the origin point with no angle or radius offset.
        """
        state = BotState()
        self.assertEqual(state.x, 0)
        self.assertEqual(state.y, 0)
        self.assertEqual(state.angle, 0)
        self.assertEqual(state.radius, 0)

if __name__ == "__main__":
    unittest.main()
