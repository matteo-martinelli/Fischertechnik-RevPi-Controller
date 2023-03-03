from MovingMachine import MovingMachine
from ReachedDirection import ReachedDirection
from Axis import AxisType, Axis
from ThreeDRobotConfig import ThreeDRobotConfig


class Robot(MovingMachine):

    def generateTransferMoveList(self, numPickup, numPlace):
        offset = 700
        # Greifer öffnen
        robotPickConf0 = ThreeDRobotConfig(self.robotSensVerticalEncoderCounter,self.robotSensRotEncoderCounter,self.__axisArm.counterValueCurrent,6,False,False,False,False)
        # Arm einfahren
        robotPickConf1 = ThreeDRobotConfig(self.robotSensVerticalEncoderCounter,self.robotSensRotEncoderCounter,0,6,False,False,True,False)
        # an Objekt heranfahren (Rot, Vertical)
        robotPickConf2 = ThreeDRobotConfig(self.placeList[numPickup][0]-offset,self.placeList[numPickup][1],0,6,False,False,True,False)
        # Arm ausfahen
        robotPickConf3 = ThreeDRobotConfig(self.placeList[numPickup][0]-offset,self.placeList[numPickup][1],self.placeList[numPickup][2],6,False,False,False,False)
        # absenken
        robotPickConf4 = ThreeDRobotConfig(self.placeList[numPickup][0],self.placeList[numPickup][1],self.placeList[numPickup][2],6,False,False,False,False)
        # Greifer schließen
        robotPickConf5 = ThreeDRobotConfig(self.placeList[numPickup][0],self.placeList[numPickup][1],self.placeList[numPickup][2],14,False,False,False,False)
        # anheben
        robotPickConf6 = ThreeDRobotConfig(self.placeList[numPickup][0]-offset,self.placeList[numPickup][1],self.placeList[numPickup][2],14,False,False,False,False)
        # Arm einfahren
        robotPlaceConf0 = ThreeDRobotConfig(self.placeList[numPickup][0]-offset,self.placeList[numPickup][1],self.placeList[numPickup][2],14,False,False,True,False)
        # bewegen
        robotPlaceConf1 = ThreeDRobotConfig(self.placeList[numPlace][0]-offset,self.placeList[numPlace][1],self.placeList[numPlace][2],14,False,False,True,False)
        # Arm ausfahren
        robotPlaceConf2 = ThreeDRobotConfig(self.placeList[numPlace][0]-offset,self.placeList[numPlace][1],self.placeList[numPlace][2],14,False,False,False,False)
        # absenken
        robotPlaceConf3 = ThreeDRobotConfig(self.placeList[numPlace][0],self.placeList[numPlace][1],self.placeList[numPlace][2],14,False,False,False,False)
        # Greifer öffnen
        robotPlaceConf4 = ThreeDRobotConfig(self.placeList[numPlace][0],self.placeList[numPlace][1],self.placeList[numPlace][2],6,False,False,False,True)
        # anheben
        robotPlaceConf5 = ThreeDRobotConfig(self.placeList[numPlace][0]-offset,self.placeList[numPlace][1],self.placeList[numPlace][2],6,False,False,True,False)
        # Arm einfahren?

        return [robotPickConf0,
                robotPickConf1,
                robotPickConf2,
                robotPickConf3,
                robotPickConf4,
                robotPickConf5,
                robotPickConf6,
                robotPlaceConf0,
                robotPlaceConf1,
                robotPlaceConf2,
                robotPlaceConf3,
                robotPlaceConf4,
                robotPlaceConf5]

    @property
    def isExecuting(self) -> bool:
        if self.__robotActRotRight or self.__robotActRotLeft or self.__robotActVerticalUp or self.__robotActVerticalDown or self.__robotActGripperOpen or self.__robotActGripperClose or self.__robotActArmOut or self.__robotActArmIn:
            return True
        else:
            return False

    #list containing all critical points on the robots path
    def __init__(self, id1, placeList):
        super().__init__(id1, placeList)
        self.__robotSensGripperOpen = self.__robotSensArmEndIn = self.__robotSensVerticalEndUp  = self.__robotSensRotEnd = False
        self.__robotActGripperOpen = self.__robotActGripperClose = self.__robotActArmOut = self.__robotActArmIn = self.__robotActVerticalDown = self.__robotActVerticalUp = self.__robotActRotRight = self.__robotActRotLeft = False
        self.__robotSensRotEncoderCounter = self.__robotSensVerticalEncoderCounter = self.__robotSensArmImpulseCounterRaw = self.__robotSensGripperImpulseCounterRaw = 0
        self.__axisArm = Axis(AxisType.Counter, 1)
        self.__axisVertical = Axis(AxisType.Encoder, 20)
        self.__axisRot = Axis(AxisType.Encoder, 20)
        self.__axisGripper = Axis(AxisType.Counter, 1)
        #self.configReached = False
        #self.setupFinished = self.setupFinishedHelper = False
        #self.__moveList = None
        #self.__pc = 0
        #self.configGoal = None

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

    def executeHelper(self):
        if self.setupFinishedHelper:
            self.setupFinishedHelper = False
            return True, True
        else:
            return False, False

    def gotoConfig(self, config):
        t1 = t2 = t3 = t4 = False
        d3 = d4 = None

        self.__axisVertical.update(self.robotSensVerticalEndUp, self.robotSensVerticalEncoderCounter)
        t1 = self.__axisVertical.gotoConfig(config.endVertical, config.counterVertical)
        self.robotActVerticalUp = self.__axisVertical.outputminus
        self.robotActVerticalDown = self.__axisVertical.outputplus

        self.__axisRot.update(self.robotSensRotEnd, self.robotSensRotEncoderCounter)
        t2 = self.__axisRot.gotoConfig(config.endRot, config.counterRot)
        self.robotActRotRight = self.__axisRot.outputminus
        self.robotActRotLeft = self.__axisRot.outputplus

        self.__axisArm.update(self.robotSensArmEndIn, self.robotSensArmImpulseCounterRaw)
        t3, d3 = self.__axisArm.gotoConfig(config.endArm, config.counterArm)
        self.robotActArmIn = self.__axisArm.outputminus
        self.robotActArmOut = self.__axisArm.outputplus

        self.__axisGripper.update(self.robotSensGripperOpen, self.robotSensGripperImpulseCounterRaw)
        t4, d4 = self.__axisGripper.gotoConfig(config.endGripper, config.counterGripper)
        self.robotActGripperOpen = self.__axisGripper.outputminus
        self.robotActGripperClose = self.__axisGripper.outputplus
        return t1 and t2 and t3 and t4
        #return ReachedDirection(t1 and t2 and t3 and t4, d3, d4)

    #referenzfahrt des Roboters um alle counter korrekt zu setzen - setzen der counter an anderer Stelle, hier aber in Referenzposition
    #von execute bereits berücksichtigt
    def setup(self):
        print("setup")
        t1 = t2 = t3 = t4 = False
        if self.robotSensArmEndIn:
            self.robotActArmIn = False
            t3 = True
        else:
            self.robotActArmIn = True

        if self.robotSensVerticalEndUp:
            self.robotActVerticalUp = False
            t1 = True
        elif t3:
            self.robotActVerticalUp = True

        if self.robotSensRotEnd:
            self.robotActRotRight = False
            t2 = True
        elif t3:
            self.robotActRotRight = True

        if self.robotSensGripperOpen:
            self.robotActGripperOpen = False
            t4 = True
        elif t3:
            self.robotActGripperOpen = True

        return (t1 and t2 and t3 and t4)

