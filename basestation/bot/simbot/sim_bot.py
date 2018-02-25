class SimBot(object):
    """
    Manages all properties of one simbot object
    """
    def __init__(self, id: int, angle: int, x: int, y: int, size: int):
        self.__angle = 0
        self.__id = 0
        self.__x = 0
        self.__y = 0
        self.__size = 0

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

