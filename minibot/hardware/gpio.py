
class PWM():

    def __init__(self, pin, frequency, duty_cycle=0):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = duty_cycle

    def set_frequency(self, frequency):
        self.frequency = frequency

    def set_duty_cycle(self, duty_cycle):
        self.duty_cycle = duty_cycle

    def stop(self):
        pass
