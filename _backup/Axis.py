from enum import Enum
from PlusMinusStop import PlusMinusStop
from ImpulseCounter import ImpulseCounter
from Counter import Counter


class AxisType(Enum):
    """used to differentiate between axis using impulse counters and encoders"""
    Counter = 1
    Encoder = 2

#TODO ensure no negative values are accepted for counter goal
class Axis:

    def __init__(self, typ: AxisType, tolerance):
        """constructor creates ImpulseCounter object if necessary"""
        self.__type = typ
        if typ == AxisType.Counter:
            self.__counter = ImpulseCounter()
        else:
            self.__counter = Counter()
        self.__tolerance = tolerance
        self.__first = True
        #variables need to be manually updated/written
        self.__endpos = 0
        self.__counterinput = 0
        self.__outputplus = 0
        self.__outputminus = 0

    @property
    def counterValueCurrent(self):
        return self.__counter.counter

    @counterValueCurrent.setter
    def counterValueCurrent(self, value):
        self.__counter.counter = value

    @property
    def endpos(self):
        return self.__endpos

    @property
    def counterinput(self):
        return self.__counterinput

    @property
    def outputplus(self):
        return self.__outputplus

    @property
    def outputminus(self):
        return self.__outputminus

    def update(self, endpos, counterinput):
        self.__endpos = endpos
        self.__counterinput = counterinput

    @staticmethod
    def howtoCounterPos(counterGoal, counterCurrent, tolerance):
        """method to determine which way the axis needs to rotate"""
        play = 10
        #"handle" overflow
        #assume overflow if counter greater 4 millions
        if counterGoal > counterCurrent + tolerance:
            return PlusMinusStop.PLUS
        elif counterGoal < counterCurrent - tolerance and counterCurrent > 4000000:
            return PlusMinusStop.PLUS
        elif counterGoal < counterCurrent - tolerance - play:
            return PlusMinusStop.MINUS
        else:
            return PlusMinusStop.STOP

    def gotoConfig(self, endpos, counterGoal):
        """method to set outputs to reach the wanted config goal for that axis"""
        t = False
        d = None
        #wenn endschalter gewünscht immer nutzen anstellen von counterGoal
        if endpos:
            if not self.__endpos:
                self.__outputminus = True
                if isinstance(self.__counter, ImpulseCounter):
                    self.__counter.counter = self.__counter.compute(self.__counterinput, PlusMinusStop.MINUS)
                    print(self.__counter.counter)
                d = PlusMinusStop.MINUS
            else:
                self.__outputminus = False
                t = True
        else:
            #calls compute methods for axis with impulse counters based on (previous) motor direction, not necessary for encoder
            if isinstance(self.__counter, ImpulseCounter):
                if self.outputplus:
                    self.__counter.counter = self.__counter.compute(self.__counterinput, PlusMinusStop.PLUS)
                    print(self.__counter.counter)
                    #print("compute counter")
                    if self.__first or self.endpos:
                        self.__first = False
                        print("Reset arm counter here here here here here here")
                        self.__counter.counter = 0
                elif self.outputminus:
                    self.__counter.counter = self.__counter.compute(self.__counterinput, PlusMinusStop.MINUS)
                    print(self.__counter.counter)
                    if self.__first or self.endpos:
                        self.__first = False
                        print("Reset arm counter here here here here here here")
                        self.__counter.counter = 0

            else:
                self.__counter.counter = self.__counterinput
            if self.howtoCounterPos(counterGoal, self.__counter.counter, self.__tolerance) == PlusMinusStop.PLUS:
                self.__outputminus = False
                self.__outputplus = True
                d = PlusMinusStop.PLUS
            elif self.howtoCounterPos(counterGoal, self.__counter.counter, self.__tolerance) == PlusMinusStop.MINUS:
                self.__outputminus = True
                self.__outputplus = False
                d = PlusMinusStop.MINUS
            elif self.howtoCounterPos(counterGoal, self.__counter.counter, self.__tolerance) == PlusMinusStop.STOP:
                self.__outputminus = False
                self.__outputplus = False
                t = True
        if isinstance(self.__counter, ImpulseCounter):
            return t, d
        return t
