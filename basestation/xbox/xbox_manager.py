import pygame
from basestation.base_station import BaseStation


class XboxManager(object):
    def __init__(self):
        pygame.joystick.init()
        self.__xboxs = {}

    def add_xbox(self, vbot_name):
        BaseStation().get_bot_manager()

    def get_detected_xbox_ids(self):
        return sorted(self.__xboxs.keys())


