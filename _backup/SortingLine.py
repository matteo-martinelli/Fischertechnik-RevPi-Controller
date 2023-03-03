from Machine import Machine
from ImpulseCounter import ImpulseCounter
from PlusMinusStop import PlusMinusStop
from Colour import Colour
from CyclicWaiter import CyclicWaiter


class SortingLine(Machine):

    #TODO self.once: implement reset possibility from execute

    @property
    def isExecuting(self) -> bool:
        return self.__packageOnLine

    def __init__(self, id1):
        super().__init__(id1)
        self.__sortingLineSensImpulseCounterRaw = 0
        self.__sortingLineSensInputLightBarrier = self.__sortingLineSensMiddleLightBarrier = self.__sortingLineSensWhiteLightBarrier = self.__sortingLineSensBlueLightBarrier = self.__sortingLineSensRedLightBarrier = True
        self.__sortingLineActMotorConveyor = self.__sortingLineActCompressorOn = self.__sortingLineActWhiteEjector = self.__sortingLineActRedEjector = self.__sortingLineActBlueEjector = False
        self.__counter = ImpulseCounter()
        self.__packageOnLine = self.__packageCountSteps = False
        self.once = True

    @property
    def sortingLineSensImpulseCounterRaw(self):
        return self.__sortingLineSensImpulseCounterRaw

    @sortingLineSensImpulseCounterRaw.setter
    def sortingLineSensImpulseCounterRaw(self, value):
        self.__sortingLineSensImpulseCounterRaw = value

    @property
    def sortingLineSensInputLightBarrier(self):
        return self.__sortingLineSensInputLightBarrier

    @sortingLineSensInputLightBarrier.setter
    def sortingLineSensInputLightBarrier(self, value):
        self.__sortingLineSensInputLightBarrier = value

    @property
    def sortingLineSensMiddleLightBarrier(self):
        return self.__sortingLineSensMiddleLightBarrier

    @sortingLineSensMiddleLightBarrier.setter
    def sortingLineSensMiddleLightBarrier(self, value):
        self.__sortingLineSensMiddleLightBarrier = value

    @property
    def sortingLineSensWhiteLightBarrier(self):
        return self.__sortingLineSensWhiteLightBarrier

    @sortingLineSensWhiteLightBarrier.setter
    def sortingLineSensWhiteLightBarrier(self, value):
        self.__sortingLineSensWhiteLightBarrier = value

    @property
    def sortingLineSensRedLightBarrier(self):
        return self.__sortingLineSensRedLightBarrier

    @sortingLineSensRedLightBarrier.setter
    def sortingLineSensRedLightBarrier(self, value):
        self.__sortingLineSensRedLightBarrier = value

    @property
    def sortingLineSensBlueLightBarrier(self):
        return self.__sortingLineSensBlueLightBarrier

    @sortingLineSensBlueLightBarrier.setter
    def sortingLineSensBlueLightBarrier(self, value):
        self.__sortingLineSensBlueLightBarrier = value

    @property
    def sortingLineActMotorConveyor(self):
        return self.__sortingLineActMotorConveyor

    @sortingLineActMotorConveyor.setter
    def sortingLineActMotorConveyor(self, value):
        self.__sortingLineActMotorConveyor = value

    @property
    def sortingLineActCompressorOn(self):
        return self.__sortingLineActCompressorOn

    @sortingLineActCompressorOn.setter
    def sortingLineActCompressorOn(self, value):
        self.__sortingLineActCompressorOn = value

    @property
    def sortingLineActWhiteEjector(self):
        return self.__sortingLineActWhiteEjector

    @sortingLineActWhiteEjector.setter
    def sortingLineActWhiteEjector(self, value):
        self.__sortingLineActWhiteEjector = value

    @property
    def sortingLineActRedEjector(self):
        return self.__sortingLineActRedEjector

    @sortingLineActRedEjector.setter
    def sortingLineActRedEjector(self, value):
        self.__sortingLineActRedEjector = value

    @property
    def sortingLineActBlueEjector(self):
        return self.__sortingLineActBlueEjector

    @sortingLineActBlueEjector.setter
    def sortingLineActBlueEjector(self, value):
        self.__sortingLineActBlueEjector = value

    @property
    def sortingLineCounterValue(self):
        return self.__counter.counter

    def startOfProcess(self, packageIncoming):
        if not self.__sortingLineSensInputLightBarrier and not self.__packageOnLine:
            self.__packageOnLine = True
            print("packageOnLine True")
        if self.__packageOnLine or packageIncoming:
            self.__packageOnLine = True
            print("packageOnLine True")
            self.__sortingLineActMotorConveyor = True
            if not self.__sortingLineSensMiddleLightBarrier:
                self.__packageCountSteps = True

    def ejectColour(self, colour):
        whiteCounter = 1
        redCounter = 7
        blueCounter = 12
        current = self.__counter.compute(self.__sortingLineSensImpulseCounterRaw, PlusMinusStop.PLUS)
        if not self.__packageCountSteps and self.once:
            self.startOfProcess(True)
            if not self.__packageCountSteps:
                self.__counter.counter = 0
        else:
            if current > blueCounter and colour == Colour.BLUE:
                self.__sortingLineActMotorConveyor = False
                self.__sortingLineActCompressorOn = True
                self.__sortingLineActBlueEjector = True
                if not self.__sortingLineSensBlueLightBarrier:
                    self.__packageOnLine = self.__packageCountSteps = False
                    print("packageOnLine False")
                    self.__sortingLineActCompressorOn = False
                    self.__sortingLineActBlueEjector = False
                    self.once = False
                    return
            if current > redCounter and colour == Colour.RED:
                self.__sortingLineActMotorConveyor = False
                self.__sortingLineActCompressorOn = True
                self.__sortingLineActRedEjector = True
                if not self.__sortingLineSensRedLightBarrier:
                    self.__packageOnLine = False
                    self.__packageCountSteps = False
                    print("packageOnLine False")
                    self.__sortingLineActCompressorOn = False
                    self.__sortingLineActRedEjector = False
                    self.once = False
                    return
            if current > whiteCounter and colour == Colour.WHITE:
                self.__sortingLineActMotorConveyor = False
                self.__sortingLineActCompressorOn = True
                self.__sortingLineActWhiteEjector = True
                if not self.__sortingLineSensWhiteLightBarrier:
                    self.__packageOnLine = self.__packageCountSteps = False
                    print("packageOnLine False")
                    self.__sortingLineActCompressorOn = False
                    self.__sortingLineActWhiteEjector = False
                    self.once = False
                    return

    def execute(self):
        self.ejectColour(Colour.RED)
