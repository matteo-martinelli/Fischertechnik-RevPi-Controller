class Counter:

    def __init__(self):
        self.__counter = 0

    @property
    def counter(self) -> int:
        return self.__counter

    @counter.setter
    def counter(self, value):
        self.__counter = value

    @counter.deleter
    def counter(self):
        self.__counter = 0
