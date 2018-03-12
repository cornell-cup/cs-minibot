class SimBot(object):
    """
    Manages all properties of one simbot object
    """
    def __init__(self, id: int, angle: int, x: int, y: int, size: int):
        self.__angle = angle
        self.__id = id
        self.__x = x
        self.__y = y
        self.__size = size

    def get_id(self):
        return self.__id

    def set_id(self, id: str):
        self.__id = id

    def get_x(self):
        return self.__x

    def set_x(self, x: int):
        self.__x = x

    def get_y(self):
        return self.__y

    def set_y(self, y: int):
        self.__y = y

    def get_angle(self):
        return self.__angle

    def set_angle(self, angle: int):
        self.__angle = angle

    def get_size(self):
        return self.__size

    def set_size(self, size: int):
        self.__size = size

    def update_direction(self, d: str):
        """
        Updates the simbot's coordinates based on input direction (f, b, l, r)

        Args:
            d (str): 'f' (forward), 'b' (backward), 'l' (left), 'r' (right)
        Returns:
            SimBot object with updated coordinates
        """
        if d == 'f':
            self.set_y(self.get_y() + 1)
        elif d == 'b':
            self.set_y(self.get_y() - 1)
        elif d == 'l':
            self.set_x(self.get_x() - 1)
        else:
            self.set_x(self.get_x() + 1)
        return self


