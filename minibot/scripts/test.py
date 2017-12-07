"""
Test script for minibot movement
"""
def run(bot):
    print("Moving Forward - 3 seconds")
    bot.move_forward(50)
    bot.wait(3)
    print("Moving Backward - 3 seconds")
    bot.move_backward(50)
    bot.wait(3)
    print("Turning Left - 3 seconds")
    bot.turn_counter_clockwise(50)
    bot.wait(3)
    print("Turning Right - 3 seconds")
    bot.turn_clockwise(50)
    bot.wait(3)
    print("Stop")
    bot.stop()
