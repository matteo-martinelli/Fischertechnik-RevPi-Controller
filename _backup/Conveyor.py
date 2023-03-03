from IllegalValueCombination import IllegalValueCombination
from Machine import Machine
from ImpulseCounter import ImpulseCounter
from PlusMinusStop import PlusMinusStop


class Conveyor(Machine):

    #TODO create reset for self.once from execute

    @property
    def isExecuting(self) -> bool:
        return not self.arrived

    def __init__(self, id1):
        super().__init__(id1)
        self.__conveyorSensImpulseCounterRaw = 0
        self.__conveyorSensLeft = self.__conveyorSensRight = True
        self.__conveyorActForward = self.__conveyorActBackward = False
        self.__counter = ImpulseCounter()
        self.current = 0
        self.arrived = False
        self.once = True

    @property
    def conveyorSensLeft(self) -> bool:
        return self.__conveyorSensLeft

    @conveyorSensLeft.setter
    def conveyorSensLeft(self, value: bool):
        self.__conveyorSensLeft = value

    @property
    def conveyorSensRight(self) -> bool:
        return self.__conveyorSensRight

    @conveyorSensRight.setter
    def conveyorSensRight(self, value: bool):
        self.__conveyorSensRight = value

    @property
    def conveyorSensImpulse(self):
        return self.__conveyorSensImpulseCounterRaw

    @conveyorSensImpulse.setter
    def conveyorSensImpulse(self, value):
        self.__conveyorSensImpulseCounterRaw = value

    @property
    def conveyorActForward(self) -> bool:
        return self.__conveyorActForward

    @conveyorActForward.setter
    def conveyorActForward(self, value: bool):
        self.__conveyorActForward = value

    @property
    def conveyorActBackward(self) -> bool:
        return self.__conveyorActBackward

    @conveyorActBackward.setter
    def conveyorActBackward(self, value: bool):
        self.__conveyorActBackward = value

    @property
    def conveyorCounterValue(self):
        return self.__counter.counter

    def forward(self):
        """Moves the package from left sensor to right sensor"""
        if not self.__conveyorSensLeft:
            self.__conveyorActForward = True
        if not self.__conveyorSensRight:
            self.__conveyorActForward = False
            return True
        return False

    def backward(self):
        """Moves the package from right sensor to left sensor"""
        if not self.__conveyorSensRight:
            self.__conveyorActBackward = True
        if not self.__conveyorSensLeft:
            self.__conveyorActBackward = False
            return True
        return False

    #TODO Once the package leaves, the conveyor is activated again automatically
    def forwardFromAnywhere(self):
        """Moves the package from any place on the conveyor to the right sensor"""
        #if self.once:
        self.__conveyorActForward = True
        if not self.__conveyorSensRight:
            self.__conveyorActForward = False
            #self.once = False
            return True
        return False

    #TODO Once the package leaves, the conveyor is activated again automatically
    def backwardFromAnywhere(self):
        """Moves the package from any place on the conveyor to the left sensor"""
        #if self.once:
        self.__conveyorActBackward = True
        if not self.__conveyorSensLeft:
            self.__conveyorActBackward = False
            #self.once = False
            return True
        return False

    def forwardLeaveConveyor(self):
        """moves the package from anywhere on the line to the left, until it leaves the conveyor"""
        #maybe use Cyclic waiter to shutoff conveyor after (50?) cycles of waiting
        #or count steps (maybe 10 extra?) after detection at left sensor
        #maybe use self.forwardFromAnywhere()
        if self.current == 0:
            self.arrived = self.forward()
            self.__counter.counter = 0
        if self.arrived:
            self.current = self.countSteps()
            self.__conveyorActForward = True
            if self.current >= 10:
                self.__conveyorActForward = False
                self.arrived = False
                self.current = 0

    def backwardLeaveConveyor(self):
        """moves the package from anywhere on the line to the right, until it leaves the conveyor"""
        #maybe use Cyclic waiter to shutoff conveyor after (50?) cycles of waiting
        #or count steps (maybe 10 extra?) after detection at right sensor
        #maybe use self.backwardFromAnywhere()
        if self.current == 0:
            self.arrived = self.backwardFromAnywhere()
            self.__counter.counter = 0
        print(self.arrived)
        if self.arrived:
            self.current = self.countSteps()
            self.__conveyorActBackward = True
            if self.current >= 10:
                self.__conveyorActBackward = False
                self.arrived = False
                #print("self.current = 0")
                self.current = 0

    def forwardHalfway(self):
        """moves the package to the middle of the conveyor starting from the left sensor"""
        self.current = self.countSteps()
        if not self.__conveyorSensLeft:
            self.__counter.counter = 0
            self.__conveyorActForward = True
        elif self.current >= 8:
            self.__conveyorActForward = False
            self.current = 0

    def backwardHalfway(self):
        """moves the package to the middle of the conveyor starting from the right sensor"""
        self.current = self.countSteps()
        if not self.__conveyorSensRight:
            self.__counter.counter = 0
            self.__conveyorActBackward = True
        elif self.current >= 8:
            self.__conveyorActBackward = False
            self.current = 0

    def countSteps(self):
        steps = self.__counter.compute(self.__conveyorSensImpulseCounterRaw, PlusMinusStop.PLUS)
        print(steps)
        return steps

    def stop(self):
        self.__conveyorActForward = self.__conveyorActBackward = False


    def execute(self):
        self.backwardLeaveConveyor()

#            self.__conveyorCounterRef = self.__conveyorCounter
#            self.__conveyorActForward = True
#        if self.__conveyorCounter - self.__conveyorCounterRef >= 10:
#            self.__conveyorActForward = False

