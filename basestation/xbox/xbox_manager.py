"""
Contains XboxManager class, which manages the connection, addition,
and removal of Xbox controllers to the device running the BaseStation.
"""

from basestation.base_station import BaseStation
from basestation.xbox.xbox import Xbox
from basestation.util.exception_handling import *
from basestation.util.class_util import Singleton

import pygame
from typing import Optional


class XboxManager(object, metaclass=Singleton):
    """
    XboxManager is a Singleton class, meaning that only instance of the
    XboxManager class can exist in a single run. The instance is an interface to
    adding, removing, and connecting Xbox Controllers to the device running the
    BaseStation.

    This class is closely coupled with the BaseStation, and has no relation with
    the code on the MiniBot side.
    """
    def __init__(self):
        """
        Initializes the XboxManager class for the first time. Since
        XboxManager is a Singleton class, repeated attempts to initialization do
        not invoke this function.
        """
        pygame.init()
        pygame.joystick.init()
        self.__xboxs = {}

    def run_xbox(self, vbot_name: str, xbox_id: int) -> Optional[int]:
        """
        Runs a Xbox instance associated with MiniBot `vbot_name`. If an Xbox
        Controller x with `x.get_id() == xbox_id` is connected to the device,
        then x is associated with the MiniBot `vbot_name`. If no such Xbox
        Controller exists, then the association operation is not performed.

        Args:
            vbot_name (str): Name of the MiniBot to associate the Xbox
                Controller.
            xbox_id (int): The ID of the Xbox Controller to be associated.

        Returns:
            (Optional[int]):
                - xbox_id if the association operation was successful
                - -1 if there doesn't exist MiniBot m with `m.get_name() ==
                    vbot_name`
                - None if there doesn't exist a Xbox Controller x such that
                    `x.get_id() == xbox_id` or the association operation failed
                    from the Xbox Controller's side.
        """
        self.__refresh_xboxs()
        vbot = BaseStation().get_bot_manager().get_bot_by_name(vbot_name)

        if vbot is None:
            # VirtualBot with vbot_name not found
            return -1
        elif xbox_id >= pygame.joystick.get_count():
            # Trying to add with an Xbox which does not exist
            return None
        else:
            try:
                xbox = self.__xboxs.get(xbox_id, None)
                if xbox is not None:
                    # update this Xbox's associated bot
                    xbox.set_assoc_bot(vbot_name)
                else:
                    # Xbox with xbox_id doesn't already exist
                    self.__xboxs[xbox_id] = Xbox(xbox_id, vbot_name)
                return xbox_id
            except RuntimeError as e:
                msg = "Xbox with " + str(xbox_id)\
                      + " could not be associated with " + vbot_name
                log_exn_info(e, msg=msg)

    def get_initialized_xbox_ids(self):
        """
        Returns a sorted (ascending) list of IDs of Xboxs that have been
        successfully associated with a MiniBot.
        """
        return sorted(self.__xboxs.keys())

    def get_detected_xbox_ids(self):
        """
        Returns a sorted (ascending) list of IDs of Xboxs that can be
        discovered on the device. Some Xboxs might not be associated with a
        MiniBot.
        """
        self.__refresh_xboxs()
        return [i for i in range(pygame.joystick.get_count())]

    def stop_xbox(self, xbox_id: int) -> bool:
        """
        Returns True if the Xbox x with `x.get_id() == xbox_id` is
        successfully removed from the XboxManager instance. Returns False if
        the operation failed, or if there does not exist an Xbox x with
        `x.get_id() == xbox_id` for all x.

        Args:
            xbox_id (int): The ID of the Xbox Controller to be removed.
        """
        xbox = self.__xboxs[xbox_id]
        try:
            del self.__xboxs[xbox_id]
        except KeyError:
            return False

        if xbox is not None:
            del xbox
            return True
        else:
            return False

    @staticmethod
    def __refresh_xboxs():
        """
        Refreshes the collection of Xbox Controllers with the currently
        connected Xbox Controllers.
        """
        pygame.joystick.init()
