import pygame
from basestation.base_station import BaseStation
import threading


class Xbox(object):

    def __init__(self, id, vbot_name):
        self.__joystick = pygame.joystick.Joystick(id)
        self.__assoc_vbot = BaseStation().get_bot_manager().\
            get_bot_by_name(vbot_name)

        if self.__assoc_vbot is None:
            self.__del__()
            raise Exception(vbot_name + " does not exist")

        threading.Thread(target=self.listen)

    def __del__(self):
        self.__joystick.quit()
        return

    def set_assoc_bot(self, vbot_name):
        self.__assoc_vbot = BaseStation().get_bot_manager().\
            get_bot_by_name(vbot_name)

        return self.__assoc_vbot is None

    def listen(self):
        pass
