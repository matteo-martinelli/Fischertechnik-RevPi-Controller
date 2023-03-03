from IllegalValueCombination import IllegalValueCombination
from Machine import Machine

class IndexedLine(Machine):

    @property
    def isExecuting(self) -> bool:
        print(self.motorSlider1Forward or self.motorSlider2Forward or self.motorSlider1Backward or self.motorSlider2Backward or self.conveyorBeltSwap or self.conveyorBeltDrilling or self.conveyorBeltMilling or self.conveyorBeltFeed or self.millingMachine or self.drillingMachine)
        return self.motorSlider1Forward or self.motorSlider2Forward or self.motorSlider1Backward or self.motorSlider2Backward or self.conveyorBeltSwap or self.conveyorBeltDrilling or self.conveyorBeltMilling or self.conveyorBeltFeed or self.millingMachine or self.drillingMachine

    def __init__(self, id1):
        super().__init__(id1)
        
        self.pushButton1Front = self.pushButton1Back =  self.pushButton2Front = self.pushButton2Back = False

        self.indexSensSlider1 = self.indexSensMilling = self.indexSensLoading = self.indexSensDrilling = self.indexSensConveyorSwap= False

        self.motorSlider1Backward = self.motorSlider1Forward = self.motorSlider2Backward = self.motorSlider2Forward = False

        self.conveyorBeltFeed = self.conveyorBeltMilling = self.millingMachine = False
        
        self.conveyorBeltDrilling = self.drillingMachine = self.conveyorBeltSwap = False
        
        self.millingCount = self.drillingCount = self.deliveryCount = 0;
        self.deliveryReady = False
        
    #Brings both sliders to the front button as it is the starting position.
    def startPosition(self):
        if not self.pushButton2Front:
            self.motorSlider2Forward= True
        else:
            self.motorSlider2Forward= False
        if not self.pushButton1Front:
            self.motorSlider1Forward= True
        else:
            self.motorSlider1Forward= False

#Brings a package from start of the indexed line onto the main conveyor.      
    def receivePackage(self):
            if not self.indexSensLoading:
                self.conveyorBeltFeed = True
            if not self.indexSensSlider1:
                self.motorSlider1Backward = True
            if self.pushButton1Back:
                self.motorSlider1Backward = False
                self.motorSlider1Forward = True
                self.conveyorBeltMilling = True
            if self.pushButton1Front:
                self.motorSlider1Forward = False
                
#The package undergoes milling.
#The millingCount is an arbitrary value.
#Change it to fit the desired number of machine rotations.
    def milling(self):
        if not self.indexSensMilling:
            if self.millingCount < 20:
                self.conveyorBeltFeed = False
                self.conveyorBeltMilling = False
                self.millingMachine = True
                self.millingCount += 1
            else:
                self.millingMachine = False
                self.conveyorBeltMilling = True
                self.conveyorBeltDrilling = True
                
#The package undergoes drilling.
#The drillingCount is an arbitrary value.
#Change it to fit the desired number of machine rotations.
#resets the milling count.
    def drilling(self):
        if not self.indexSensDrilling:
            if self.drillingCount < 20:
                self.conveyorBeltMilling = False
                self.conveyorBeltDrilling = False
                self.drillingMachine = True
                self.drillingCount += 1
            else:
                self.drillingMachine = False
                self.conveyorBeltDrilling= True
                self.millingCount = 0
            
#Brings the package from the drilling machine to
#the conveyor belt at the end of the indexed line.
#resets the drilling count.
    def deliverPackage(self):
        if not self.indexSensDrilling and self.drillingCount >= 20:
            self.motorSlider2Backward = True
            self.conveyorBeltSwap = True
        if self.pushButton2Back:
            self.motorSlider2Backward = False
            self.motorSlider2Forward = True
        if self.pushButton2Front:
            self.motorSlider2Forward = False
        if not self.indexSensConveyorSwap:
            self.conveyorBeltDrilling= False
            self.deliveryReady = True
            self.drillingCount = 0
            
#Brings the package from the start of the indexed line.
#The package is drilled and milled by the respecting machines.
#Then the package is brought to the end of the indexed line.
    def processPackage(self):
            self.receivePackage()
            self.milling()
            self.drilling()
            self.deliverPackage()
            self.finishDelivery()
            
#Stops the belt at the end of the indexed line.
#Condition is activated upon reaching the sensor
#at the swap conveyer.
    def finishDelivery(self):
        if self.deliveryReady:
            self.deliveryCount += 1
            if self.deliveryCount >= 50:
                self.conveyorBeltSwap = False
                self.deliveryReady = False
                self.deliveryCount = 0

    def execute(self, *args):
        self.processPackage()
