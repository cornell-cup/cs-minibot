import unittest

from minibot.botstate import BotState

class TestBotBasics(unittest.TestCase):

    def test_default_state(self):
        state = BotState()
        self.assertEqual(state.x, 0)
        self.assertEqual(state.y, 0)
        self.assertEqual(state.angle, 0)
        self.assertEqual(state.radius, 0)

if __name__ == "__main__":
    unittest.main()
