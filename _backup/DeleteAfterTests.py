#from IllegalValueCombination import IllegalValueCombination
from Machine import Machine
#from time import sleep
from PlusMinusStop import PlusMinusStop
#from ThreeDRobotConfig import ThreeDRobotConfig
from ReachedDirection import ReachedDirection
from ImpulseCounter import ImpulseCounter
#from RobotMovementManager import RobotMovementManager


class RobotTester(Machine):

    @property
    def isExecuting(self) -> bool:
        if self.__robotActRotRight or self.__robotActRotLeft or self.__robotActVerticalUp or self.__robotActVerticalDown or self.__robotActGripperOpen or self.__robotActGripperClose or self.__robotActArmOut or self.__robotActArmIn:
            return True
        else:
            return False

    #dict containing all critical points on the robots path
    def __init__(self, id1):
        super().__init__(id1)
        self.__robotSensGripperOpen = self.__robotSensArmEndIn = self.__robotSensVerticalEndUp  = self.__robotSensRotEnd = False
        self.__robotActGripperOpen = self.__robotActGripperClose = self.__robotActArmOut = self.__robotActArmIn = self.__robotActVerticalDown = self.__robotActVerticalUp = self.__robotActRotRight = self.__robotActRotLeft = False
        self.__robotSensRotEncoderCounter = self.__robotSensVerticalEncoderCounter = self.__robotSensArmImpulseCounterRaw = self.__robotSensGripperImpulseCounterRaw = 0
        self.__robotSensArmImpulseCounter = self.__robotSensGripperImpulseCounter = 0
        self.__armImpulseCounter = ImpulseCounter()
        self.__gripperImpulseCounter = ImpulseCounter()
        self.configReached = False
        self.setupFinished = self.setupFinishedHelper = False
        #self.__moveList = moveList
        self.__pc = 0
        self.configGoal = None

    @property
    def robotSensGripperOpen(self) -> bool:
        return self.__robotSensGripperOpen

    @robotSensGripperOpen.setter
    def robotSensGripperOpen(self, value):
        self.__robotSensGripperOpen = value

    @property
    def robotSensGripperImpulseCounterRaw(self) -> int:
        return self.__robotSensGripperImpulseCounterRaw

    @robotSensGripperImpulseCounterRaw.setter
    def robotSensGripperImpulseCounterRaw(self, value):
        self.__robotSensGripperImpulseCounterRaw = value

    @property
    def robotSensArmEndIn(self) -> bool:
        return self.__robotSensArmEndIn

    @robotSensArmEndIn.setter
    def robotSensArmEndIn(self, value):
        self.__robotSensArmEndIn = value

    @property
    def robotSensArmImpulseCounterRaw(self) -> int:
        return self.__robotSensArmImpulseCounterRaw

    @robotSensArmImpulseCounterRaw.setter
    def robotSensArmImpulseCounterRaw(self, value):
        self.__robotSensArmImpulseCounterRaw = value

    @property
    def robotSensVerticalEndUp(self) -> bool:
        return self.__robotSensVerticalEndUp

    @robotSensVerticalEndUp.setter
    def robotSensVerticalEndUp(self, value):
        self.__robotSensVerticalEndUp = value

    @property
    def robotSensVerticalEncoderCounter(self):
        return self.__robotSensVerticalEncoderCounter

    @robotSensVerticalEncoderCounter.setter
    def robotSensVerticalEncoderCounter(self, value):
        self.__robotSensVerticalEncoderCounter = value

    @property
    def robotSensRotEnd(self):
        return self.__robotSensRotEnd

    @robotSensRotEnd.setter
    def robotSensRotEnd(self, value):
        self.__robotSensRotEnd = value

    @property
    def robotSensRotEncoderCounter(self):
        return self.__robotSensRotEncoderCounter

    @robotSensRotEncoderCounter.setter
    def robotSensRotEncoderCounter(self, value):
        self.__robotSensRotEncoderCounter = value

    @property
    def robotActGripperOpen(self):
        return self.__robotActGripperOpen

    @robotActGripperOpen.setter
    def robotActGripperOpen(self, value):
        self.__robotActGripperOpen = value

    @property
    def robotActGripperClose(self):
        return self.__robotActGripperClose

    @robotActGripperClose.setter
    def robotActGripperClose(self, value):
        self.__robotActGripperClose = value

    @property
    def robotActArmOut(self):
        return self.__robotActArmOut

    @robotActArmOut.setter
    def robotActArmOut(self, value):
        self.__robotActArmOut = value

    @property
    def robotActArmIn(self):
        return self.__robotActArmIn

    @robotActArmIn.setter
    def robotActArmIn(self, value):
        self.__robotActArmIn = value

    @property
    def robotActVerticalDown(self):
        return self.__robotActVerticalDown

    @robotActVerticalDown.setter
    def robotActVerticalDown(self, value):
        self.__robotActVerticalDown = value

    @property
    def robotActVerticalUp(self):
        return self.__robotActVerticalUp

    @robotActVerticalUp.setter
    def robotActVerticalUp(self, value):
        self.__robotActVerticalUp = value

    @property
    def robotActRotRight(self):
        return self.__robotActRotRight

    @robotActRotRight.setter
    def robotActRotRight(self, value):
        self.__robotActRotRight = value

    @property
    def robotActRotLeft(self):
        return self.__robotActRotLeft

    @robotActRotLeft.setter
    def robotActRotLeft(self, value):
        self.__robotActRotLeft = value

    @property
    def robotSensArmImpulseCounter(self):
        return self.__robotSensArmImpulseCounter

    @robotSensArmImpulseCounter.setter
    def robotSensArmImpulseCounter(self, value):
        self.__robotSensArmImpulseCounter = value

    @property
    def robotSensGripperImpulseCounter(self):
        return self.__robotSensGripperImpulseCounter

    @robotSensGripperImpulseCounter.setter
    def robotSensGripperImpulseCounter(self, value):
        self.__robotSensGripperImpulseCounter = value
