import socket
import traceback


class TCPConnection(object):

    def __init__(self, ip, port):
        """
        Initialize a TCP connection between this basestation and the the
        device identified by IP on the local network at port

        Args:
            ip (str): The IP of the device to be connected with this device
            port (int): The port of the connection
        """
        self.__IP = ip
        self.__port = port
        try:
            # todo: setup the TCP connection
            self.__connection_refused = False

        except socket.error as e:
            print("Unable to establish TCP Connection with " + self.__IP + ".")
            traceback.print_tb(e.__traceback__)
            self.__connection_refused = True

        return
