from Counter import Counter
from PlusMinusStop import PlusMinusStop


class ImpulseCounter(Counter):

    def __init__(self):
        super().__init__()
        self.counter = 0
        self.__dirForward = self.__dirBackward = False
        self.__numalt = 0

    @property
    def dirForward(self):
        return self.__dirForward

    @property
    def dirBackward(self):
        return self.__dirBackward

    def compute(self, num, direction):
        if direction == PlusMinusStop.PLUS:
            self.counter += (num - self.__numalt)
        elif direction == PlusMinusStop.MINUS:
            self.counter -= (num - self.__numalt)
        self.__numalt = num
        return self.counter
