from Machine import Machine


class PunchingMachine(Machine):

    def __init__(self, id1):
        super().__init__(id1)
        self.__punchingSensLeft = False
        self.__punchingSensRight = False
        self.__punchingMachineIsUp = False
        self.__punchingMachineIsDown = False
        self.__punchingActForward = False
        self.__punchingActBackward = False
        self.__punchingMachineMoveUp = False
        self.__punchingMachineMoveDown = False
        self.__packageProcessed = False

#self.__packageProcessed is here as a reminder to reset it for the next run
#of the punching machine.
    @property
    def isExecuting(self) -> bool:
        if self.__punchingActForward or self.__punchingActBackward \
                or self.__punchingMachineMoveUp or self.__punchingMachineMoveDown or self.__packageProcessed:
            return True
        else:
            return False

    @property
    def punchingSensLeft(self) -> bool:
        return self.__punchingSensLeft

    @punchingSensLeft.setter
    def punchingSensLeft(self, value: bool):
        self.__punchingSensLeft = value

    @property
    def punchingSensRight(self) -> bool:
        return self.__punchingSensRight

    @punchingSensRight.setter
    def punchingSensRight(self, value: bool):
        self.__punchingSensRight = value
        
    @property
    def punchingMachineIsUp(self) -> bool:
        return self.__punchingMachineIsUp

    @punchingMachineIsUp.setter
    def punchingMachineIsUp(self, value: bool):
        self.__punchingMachineIsUp = value

    @property
    def punchingMachineIsDown(self) -> bool:
        return self.__punchingMachineIsDown

    @punchingMachineIsDown.setter
    def punchingMachineIsDown(self, value: bool):
        self.__punchingMachineIsDown = value
        
    @property
    def punchingActForward(self) -> bool:
        return self.__punchingActForward

    @punchingActForward.setter
    def punchingActForward(self, value: bool):
        self.__punchingActForward = value

    @property
    def punchingActBackward(self) -> bool:
        return self.__punchingActBackward

    @punchingActBackward.setter
    def punchingActBackward(self, value: bool):
        self.__punchingActBackward = value
        
    @property
    def punchingMachineMoveUp(self) -> bool:
        return self.__punchingMachineMoveUp

    @punchingMachineMoveUp.setter
    def punchingMachineMoveUp(self, value: bool):
        self.__punchingMachineMoveUp = value

    @property
    def punchingMachineMoveDown(self) -> bool:
        return self.__punchingMachineMoveDown

    @punchingMachineMoveDown.setter
    def punchingMachineMoveDown(self, value: bool):
        self.__punchingMachineMoveDown = value
        
    @property
    def packageProcessed(self) -> bool:
        return self.__packageProcessed

    @packageProcessed.setter
    def packageProcessed(self, value: bool):
        self.__packageProcessed = value

#Moves the package from the left sensor to the punching machine.
    def receive(self):
        if not self.__packageProcessed:
            if not self.__punchingSensLeft:
                self.__punchingActForward = True
            if not self.__punchingSensRight:
                self.__punchingActForward = False
                
#Moves the package from the punching machine to the left sensor.
    def deliver(self):
        if self.__packageProcessed:
            if not self.__punchingSensRight:
                self.__punchingActBackward = True
            if not self.__punchingSensLeft:
                self.__punchingActBackward = False

#Moves the punching machine down and then up on the package.
#Sets the self.__packageProcessed flag to True
    def process(self):
        if not self.__punchingSensRight or self.__packageProcessed:
            if not self.__packageProcessed:
                if not self.__punchingMachineIsDown:
                    self.__punchingMachineMoveDown = True
                else:
                    self.__punchingMachineMoveDown = False
                    self.__packageProcessed = True
            else:
                if not self.__punchingMachineIsUp:
                    self.__punchingMachineMoveUp = True
                else:
                    self.__punchingMachineMoveUp = False
                    
#Stops the package at the punching Machine.
#Use this if you need to activate the conveyor
#before the package reaches the sensor.
    def receiveFrom(self, destination):
        if not self.__packageProcessed:
            if not destination:
                self.__punchingActForward = True
            if not self.__punchingSensRight:
                self.__punchingActForward = False
             
#Activates the punching Machine
#Once the package finishes processing
#Use this if you don't need to stop it
#upon reaching the right sensor.
    def deliverTo(self, destination):
        if self.__packageProcessed:
            if not self.__punchingSensRight:
                self.__punchingActBackward = True
            if not destination:
                self.__punchingActBackward = False

#Moves the package to the punching machine.
#The machine then processes the package.
#After that the package is returned to the
#starting position at the conveyor.
    def processPackage(self):
        self.receive()
        self.process()
        self.deliver()

#Use this operation if the punching machine is connected
#to another one e.g. a conveyor
    def processPackageFrom(self, destination):
        self.receiveFrom(destination)
        self.process()
        self.deliverTo(destination)
        
#Use this operation if the incoming and outgoing
#destinations are different
    def processPackageFromTo(self, incoming, outgoing):
        self.receiveFrom(incoming)
        self.process()
        self.deliverTo(outgoing)
        
#Resets the packageProcessed flag to False
#Since it is set to True after the punching machine
#does the processing.
    def resetMachine(self):
        self.__packageProcessed = False