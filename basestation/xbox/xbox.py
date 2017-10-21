from basestation.base_station import BaseStation
from basestation.util.exception_handling import *

import pygame
import threading


class Xbox(object):

    def __init__(self, xbox_id, vbot_name):
        self.__joystick = pygame.joystick.Joystick(xbox_id)
        self.__assoc_vbot = BaseStation().get_bot_manager().\
            get_bot_by_name(vbot_name)

        if self.__assoc_vbot is None:
            self.__del__()
            raise RuntimeError(vbot_name + " does not exist")

        self.__xbox_listener = threading.Thread(target=self.listen)
        return

    def __del__(self):
        """
        Deletes this instance of Xbox interface to the controller.
        """
        self.__joystick.quit()
        self.__xbox_listener.join()
        return

    def get_xbox_id(self):
        return self.__joystick.get_id()

    def get_xbox_name(self):
        return self.__joystick.get_name()

    def set_assoc_bot(self, vbot_name):
        self.__assoc_vbot = BaseStation().get_bot_manager().\
            get_bot_by_name(vbot_name)

        return self.__assoc_vbot is None

    def listen(self):
        try:
            while True:
                axes = self.__joystick.get_numaxes()
                buttons = self.__joystick.get_numbuttons()
                dpad = self.__joystick.get_numhats()
                # todo: do things with axes, buttons and dpads

        except RuntimeError as e:
            msg = "Unable to get input from Xbox with ID = "\
                  + str(self.get_xbox_id())
            log_exn_info(e, msg=msg)



