from basestation.base_station import BaseStation
from basestation.util.exception_handling import *

import pygame
import threading
import enum


class Direction(enum.Enum):
    FORWARD = object()
    RIGHT_FORWARD = object()
    BACKWARD = object()
    LEFT_FORWARD = object()
    STOP = object()


class Xbox(object):

    max_motor_pow = 100.

    def __init__(self, xbox_id, vbot_name):
        self.__joystick = pygame.joystick.Joystick(xbox_id)
        self.__assoc_vbot = BaseStation().get_bot_manager().\
            get_bot_by_name(vbot_name)

        if self.__assoc_vbot is None:
            self.__del__()
            raise RuntimeError(vbot_name + " does not exist")

        self.__xbox_listener = threading.Thread(target=self.__listen)
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

    def __listen(self):
        try:
            while True:
                dpad_val = self.__joystick.get_hat(0)
                if dpad_val != (0, 0):
                    # dpad is pressed
                    self.__dpad_parse(dpad_val)

                # take y values of the thumbs
                # for some weird reason, pushing up the thumbs produces
                # negative values
                left_thumb_val = -self.__joystick.get_axis(1)
                right_thumb_val = -self.__joystick.get_axis(3)
                self.__thumbs_parse(left_thumb_val, right_thumb_val)

        except RuntimeError as e:
            msg = "Unable to get input from Xbox with ID = "\
                  + str(self.get_xbox_id())
            log_exn_info(e, msg=msg)

    def __dpad_parse(self, dpad_arr):
        x, y = dpad_arr[0], dpad_arr[1]
        if y > 0:
            return self.__move_bot_four_dir(Direction.FORWARD)
        elif y < 0:
            return self.__move_bot_four_dir(Direction.BACKWARD)
        elif x > 0:
            return self.__move_bot_four_dir(Direction.RIGHT_FORWARD)
        elif x < 0:
            return self.__move_bot_four_dir(Direction.LEFT_FORWARD)
        else:
            # x == 0 and y == 0
            return self.__move_bot_four_dir(Direction.STOP)

    def __thumbs_parse(self, left_thumb, right_thumb):
        self.__move_bot(left_thumb * self.max_motor_pow,
                        right_thumb * self.max_motor_pow, 0., 0.)

    def __move_bot_four_dir(self, direction):
        if direction is Direction.FORWARD:
            self.__move_bot(self.max_motor_pow, self.max_motor_pow,
                            self.max_motor_pow, self.max_motor_pow)
        elif direction is Direction.BACKWARD:
            self.__move_bot(-self.max_motor_pow, -self.max_motor_pow,
                            -self.max_motor_pow, -self.max_motor_pow)
        elif direction is Direction.RIGHT_FORWARD:
            self.__move_bot(self.max_motor_pow, -self.max_motor_pow,
                            self.max_motor_pow, -self.max_motor_pow)
        elif direction is Direction.LEFT_FORWARD:
            self.__move_bot(-self.max_motor_pow, self.max_motor_pow,
                            -self.max_motor_pow, self.max_motor_pow)
        else:
            # dir is Direction.STOP
            self.__move_bot(0., 0., 0., 0.)

    def __move_bot(self, fl, fr, bl, br):
        return self.__assoc_vbot.get_command_center().\
                set_wheel_power(fl, fr, bl, br)
