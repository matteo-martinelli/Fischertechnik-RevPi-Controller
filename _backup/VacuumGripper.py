from MovingMachine import MovingMachine
from Axis import AxisType, Axis
from VacuumGripperConfig import VacuumGripperConfig
from CyclicWaiter import CyclicWaiter
from math import isclose


class VacuumGripper(MovingMachine):

    def generateTransferMoveList(self, numPickup, numPlace):
        offset = 250
        # Arm einfahren
        robotPickConf0 = VacuumGripperConfig(self.vacuumSensVerticalEncoderCounter, self.vacuumSensRotEncoderCounter, 0, False)
        # bewegen
        robotPickConf1 = VacuumGripperConfig(self.placeList[numPickup][0]-offset, self.placeList[numPickup][1], 0, False)
        # Arm ausfahen
        robotPickConf2 = VacuumGripperConfig(self.placeList[numPickup][0]-offset, self.placeList[numPickup][1], self.placeList[numPickup][2], False)
        if isclose(self.vacuumSensVerticalEncoderCounter, self.placeList[numPickup][0]-offset, abs_tol=20) and isclose(self.vacuumSensRotEncoderCounter, self.placeList[numPickup][1], abs_tol=20):
            robotPickConf0 = robotPickConf2
            robotPickConf1 = robotPickConf2
        # von oben heran
        robotPickConf3 = VacuumGripperConfig(self.placeList[numPickup][0]+offset, self.placeList[numPickup][1], self.placeList[numPickup][2], False)
        # greifen
        robotPickConf4 = VacuumGripperConfig(self.placeList[numPickup][0]+offset, self.placeList[numPickup][1], self.placeList[numPickup][2], True)
        # nach oben
        robotPickConf5 = VacuumGripperConfig(self.placeList[numPickup][0]-offset, self.placeList[numPickup][1], self.placeList[numPickup][2], True)
        # Arm einfahren
        robotPlaceConf0 = VacuumGripperConfig(self.placeList[numPickup][0]-offset, self.placeList[numPickup][1], 0, True)
        # bewegen
        robotPlaceConf1 = VacuumGripperConfig(self.placeList[numPlace][0]-offset, self.placeList[numPlace][1], 0, True)
        # Arm ausfahren
        robotPlaceConf2 = VacuumGripperConfig(self.placeList[numPlace][0]-offset, self.placeList[numPlace][1], self.placeList[numPlace][2], True)
        # von oben heran
        robotPlaceConf3 = VacuumGripperConfig(self.placeList[numPlace][0]+offset, self.placeList[numPlace][1], self.placeList[numPlace][2], True)
        # loslassen
        robotPlaceConf4 = VacuumGripperConfig(self.placeList[numPlace][0]+offset, self.placeList[numPlace][1], self.placeList[numPlace][2], False)
        # nach oben
        robotPlaceConf5 = VacuumGripperConfig(self.placeList[numPlace][0]-offset, self.placeList[numPlace][1], self.placeList[numPlace][2], False)

        return [robotPickConf0,
                robotPickConf1,
                robotPickConf2,
                robotPickConf3,
                robotPickConf4,
                robotPickConf5,
                robotPlaceConf0,
                robotPlaceConf1,
                robotPlaceConf2,
                robotPlaceConf3,
                robotPlaceConf4,
                robotPlaceConf5]

    @property
    def isExecuting(self) -> bool:
        if self.__vacuumActRotRight or self.__vacuumActRotLeft or self.__vacuumActVerticalUp or self.__vacuumActVerticalDown or self.__vacuumActCompressorOn or self.__vacuumActValve or self.__vacuumActArmOut or self.__vacuumActArmIn:
            return True
        else:
            return False

    def __init__(self, id1, placeList):
        super().__init__(id1, placeList)
        self.__vacuumSensArmEndIn = self.__vacuumSensVerticalEndUp  = self.__vacuumSensRotEnd = False
        self.__vacuumActArmOut = self.__vacuumActArmIn = self.__vacuumActVerticalDown = self.__vacuumActVerticalUp = self.__vacuumActRotRight = self.__vacuumActRotLeft = self.__vacuumActCompressorOn = self.__vacuumActValve = False
        self.__vacuumSensRotEncoderCounter = self.__vacuumSensVerticalEncoderCounter = self.__vacuumSensArmEncoderCounter = 0
        self.__axisArm = Axis(AxisType.Encoder, 20)
        self.__axisVertical = Axis(AxisType.Encoder, 20)
        self.__axisRot = Axis(AxisType.Encoder, 20)
        self.__gripperWaiter = CyclicWaiter(10)
        self.configReached = False
        self.setupFinished = self.setupFinishedHelper = False
        self.__moveList = None
        self.__pc = 0
        self.configGoal = None


    @property
    def vacuumActCompressorOn(self):
        return self.__vacuumActCompressorOn

    @vacuumActCompressorOn.setter
    def vacuumActCompressorOn(self, value):
        self.__vacuumActCompressorOn = value

    @property
    def vacuumActValve(self):
        return self.__vacuumActValve

    @vacuumActValve.setter
    def vacuumActValve(self, value):
        self.__vacuumActValve = value

    @property
    def vacuumSensVerticalEndUp(self) -> bool:
        return self.__vacuumSensVerticalEndUp

    @vacuumSensVerticalEndUp.setter
    def vacuumSensVerticalEndUp(self, value):
        self.__vacuumSensVerticalEndUp = value

    @property
    def vacuumSensVerticalEncoderCounter(self):
        return self.__vacuumSensVerticalEncoderCounter

    @vacuumSensVerticalEncoderCounter.setter
    def vacuumSensVerticalEncoderCounter(self, value):
        self.__vacuumSensVerticalEncoderCounter = value

    @property
    def vacuumSensArmEndIn(self) -> bool:
        return self.__vacuumSensArmEndIn

    @vacuumSensArmEndIn.setter
    def vacuumSensArmEndIn(self, value):
        self.__vacuumSensArmEndIn = value

    @property
    def vacuumSensArmEncoderCounter(self):
        return self.__vacuumSensArmEncoderCounter

    @vacuumSensArmEncoderCounter.setter
    def vacuumSensArmEncoderCounter(self, value):
        self.__vacuumSensArmEncoderCounter = value

    @property
    def vacuumSensRotEnd(self):
        return self.__vacuumSensRotEnd

    @vacuumSensRotEnd.setter
    def vacuumSensRotEnd(self, value):
        self.__vacuumSensRotEnd = value

    @property
    def vacuumSensRotEncoderCounter(self):
        return self.__vacuumSensRotEncoderCounter

    @vacuumSensRotEncoderCounter.setter
    def vacuumSensRotEncoderCounter(self, value):
        self.__vacuumSensRotEncoderCounter = value

    @property
    def vacuumActArmOut(self):
        return self.__vacuumActArmOut

    @vacuumActArmOut.setter
    def vacuumActArmOut(self, value):
        self.__vacuumActArmOut = value

    @property
    def vacuumActArmIn(self):
        return self.__vacuumActArmIn

    @vacuumActArmIn.setter
    def vacuumActArmIn(self, value):
        self.__vacuumActArmIn = value

    @property
    def vacuumActVerticalDown(self):
        return self.__vacuumActVerticalDown

    @vacuumActVerticalDown.setter
    def vacuumActVerticalDown(self, value):
        self.__vacuumActVerticalDown = value

    @property
    def vacuumActVerticalUp(self):
        return self.__vacuumActVerticalUp

    @vacuumActVerticalUp.setter
    def vacuumActVerticalUp(self, value):
        self.__vacuumActVerticalUp = value

    @property
    def vacuumActRotRight(self):
        return self.__vacuumActRotRight

    @vacuumActRotRight.setter
    def vacuumActRotRight(self, value):
        self.__vacuumActRotRight = value

    @property
    def vacuumActRotLeft(self):
        return self.__vacuumActRotLeft

    @vacuumActRotLeft.setter
    def vacuumActRotLeft(self, value):
        self.__vacuumActRotLeft = value

    def executeHelper(self):
        if self.setupFinishedHelper:
            self.setupFinishedHelper = False
            return True, True, True
        else:
            return False, False, True

    def gotoConfig(self, config):
        t1 = t2 = t3 = t4 = False
        d3 = None

        self.__axisVertical.update(self.vacuumSensVerticalEndUp, self.vacuumSensVerticalEncoderCounter)
        t1 = self.__axisVertical.gotoConfig(config.endVertical, config.counterVertical)
        self.vacuumActVerticalUp = self.__axisVertical.outputminus
        self.vacuumActVerticalDown = self.__axisVertical.outputplus

        self.__axisRot.update(self.vacuumSensRotEnd, self.vacuumSensRotEncoderCounter)
        t2 = self.__axisRot.gotoConfig(config.endRot, config.counterRot)
        self.vacuumActRotRight = self.__axisRot.outputminus
        self.vacuumActRotLeft = self.__axisRot.outputplus

        self.__axisArm.update(self.vacuumSensArmEndIn, self.vacuumSensArmEncoderCounter)
        t3 = self.__axisArm.gotoConfig(config.endArm, config.counterArm)
        self.vacuumActArmIn = self.__axisArm.outputminus
        self.vacuumActArmOut = self.__axisArm.outputplus

        if config.gripperActive:
            self.__vacuumActCompressorOn = True
            self.__vacuumActValve = True
            t4 = self.__gripperWaiter.wait()
        else:
            self.__vacuumActCompressorOn = False
            self.__vacuumActValve = False
            t4 = True

        return (t1 and t2 and t3 and t4)

    #referenzfahrt des vacuumers um alle counter korrekt zu setzen - setzen der counter an anderer Stelle, hier aber in Referenzposition
    #von execute bereits berücksichtigt
    def setup(self):
        t1 = t2 = t3 = False
        if self.vacuumSensArmEndIn:
            self.vacuumActArmIn = False
            t3 = True
        else:
            self.vacuumActArmIn = True

        if self.vacuumSensVerticalEndUp:
            self.vacuumActVerticalUp = False
            t1 = True
        elif t3:
            self.vacuumActVerticalUp = True

        if self.vacuumSensRotEnd:
            self.vacuumActRotRight = False
            t2 = True
        elif t3:
            self.vacuumActRotRight = True

        self.vacuumActCompressorOn = False
        self.vacuumActValve = False

        return (t1 and t2 and t3)

