#from multipledispatch import dispatch
from math import sqrt


class PositionCartesian:
    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def z(self):
        return self.__x

    @z.setter
    def z(self, value):
        self.__z = value

    def distFrom(self, x, y, z) -> float:
        dist = sqrt(pow(self.__x - x, 2) + pow(self.__y - y, 2) + pow(self.__z - z, 2))
        return dist


