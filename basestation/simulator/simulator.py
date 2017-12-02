"""
Class that contains simulator related stuff
"""

class Simulator:
    def __init__(self):
        self.listOfScenario = []

    def set_scenario_list(self, list):
        self.listOfScenario = list

    def get_scenario_list(self):
        return self.listOfScenario