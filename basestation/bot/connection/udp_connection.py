from basestation.util.exception_handling import *

import threading
import time
import socket


class UDPConnection(threading.Thread):
    """
    UDPConnection's instances can be used to track devices that are
    broadcasting on a certain internally-set port. Can be used to discovering
    MiniBots that are currently actively broadcasting signals through UDP.
    """

    def __init__(self, group=None, target=None, name=None, args=(),
                 kwargs=None):
        super().__init__(group=group, target=target, name=name, args=args,
                         kwargs=kwargs)
        # the time (sec) before an address is removed from our list
        self.__update_threshold = 40.0
        self.__port = 5001
        self.__IP_list = {}

        self.__listener_socket = socket.socket(socket.AF_INET,
                                               socket.SOCK_DGRAM)
        self.__listener_socket.bind(('', self.__port))

        return

    def get_addresses(self):

        self.__clean_addresses()
        return sorted(self.__IP_list.keys())

    def run(self):
        try:
            while True:
                # todo: udp listener not working, blocking statement. When
                # changed to non-blocking, gives an error
                data = self.__listener_socket.recvfrom(1024)
                device_address = data[1][0]
                print("a")
                self.__IP_list[device_address] = self.__get_current_time()

        except socket.error as e:
            msg = "Unable to receive broadcasts sent to the port " + \
                  str(self.__port) + "."
            log_exn_info(e, msg)

        return

    def __clean_addresses(self):

        now = self.__get_current_time()
        new_IP_list = {}

        for address, last_updated_time in self.__IP_list.items():
            if now - last_updated_time <= self.__update_threshold:
                new_IP_list[address] = last_updated_time

        self.__IP_list = new_IP_list
        return

    @staticmethod
    def __get_current_time():
        return time.time()
