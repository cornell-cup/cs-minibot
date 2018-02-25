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

