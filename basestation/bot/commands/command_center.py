import json


class CommandCenter(object):
    """
    An instance whose methods are all the commands that can be issued to a vbot.
    Each VirtualBot must implement this class with their own commands.
    """

    def __init__(self, connection_obj):
        self.__connection = connection_obj
        self.__record = False
        return

    def toggle_logging(self):
        """
        Toggle data logging
        """
        self.__record = True
        return

    def is_logging(self):
        """
        Returns:
             (bool): true is the data is being logged, false otherwise
        """
        return self.__record

    def sendKV(self, key, value):
        """
        Sends an arbitrary key and value over the associated bot's connection

        Args:
            key (str): A key to identify the type of command
            value (str): A string that qualifies the key

        Returns:
            (bool): true if the command "seemed" to have been sent correctly
        """
        return self.__connection.sendKV(key, value)

    def get_all_data(self):
        # todo: not implemented yet
        return None

    def set_wheel_power(self, fl, fr, bl, br):
        """
        Sets the wheel power for all four wheels. Wheel power should be a number
        from -100 to 100. Negative number implies that the wheel is moving
        backwards.

        Args:
            fl (float): power to set the front left wheel.
            fr (float): power to set the front right wheel.
            bl (float): power to set the back left wheel.
            br (float): power to set the back right wheel.

        Returns:
            (bool): true if the command was successful sent to the MiniBot.
                There is no guarantee that the MiniBot-side programs will
                respond to the sent instructions correctly.
        """
        return self.sendKV("WHEELS", str(fl) + "," + str(fr) + "," + str(
            bl) + "," + str(br))

    def get_connection(self):
        return self.__connection
