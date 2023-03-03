from Machine import Machine
from MovingMachine import MovingMachine
from WarehouseConfig import WarehouseConfig
from Axis import AxisType, Axis


class Warehouse(MovingMachine):

    def generateTransferMoveList(self, numPickup, numPlace):
        offset = 50
        # (sicherheitshalber) Arm einfahren
        warehousePickConf0 = WarehouseConfig(self.warehouseSensEncoderVertical, self.warehouseSensEncoderHorizontal,True,False,False,False)
        # mit eingefahrenem Arm in Ladepos
        warehousePickConf1 = WarehouseConfig(self.placeList[numPickup][0]+offset, self.placeList[numPickup][1],True,False,False,False)
        # Arm ausfahren
        warehousePickConf2 = WarehouseConfig(self.placeList[numPickup][0]+offset, self.placeList[numPickup][1],False,True,False,False)
        # Förderband aktivieren
        if numPickup == 0:
            warehousePickConf3 = WarehouseConfig(self.placeList[numPickup][0]+offset, self.placeList[numPickup][1],False,True,True,False)
        else:
            warehousePickConf3 = warehousePickConf2
        # anheben
        warehousePickConf4 = WarehouseConfig(self.placeList[numPickup][0]-offset, self.placeList[numPickup][1],False,True,False,False)
        # Arm einfahren
        warehousePickConf5 = WarehouseConfig(self.placeList[numPickup][0]-offset, self.placeList[numPickup][1],True,False,False,False)
        # move
        warehousePlaceConf0 = WarehouseConfig(self.placeList[numPlace][0]-offset, self.placeList[numPlace][1],True,False,False,False)
        # Arm ausfahren
        warehousePlaceConf1 = WarehouseConfig(self.placeList[numPlace][0]-offset, self.placeList[numPlace][1],False,True,False,False)
        # absenken
        warehousePlaceConf2 = WarehouseConfig(self.placeList[numPlace][0]+offset, self.placeList[numPlace][1],False,True,False,False)
        #Förderband aktivieren
        if numPlace == 0:
            warehousePlaceConf3 = WarehouseConfig(self.placeList[numPlace][0]+offset, self.placeList[numPlace][1],False,True,False,True)
        else:
            warehousePlaceConf3 = warehousePlaceConf2
        # Arm einfahren
        warehousePlaceConf4 = WarehouseConfig(self.placeList[numPlace][0]+offset, self.placeList[numPlace][1],True,False,False,False)

        return [warehousePickConf0,
                warehousePickConf1,
                warehousePickConf2,
                warehousePickConf3,
                warehousePickConf4,
                warehousePickConf5,
                warehousePlaceConf0,
                warehousePlaceConf1,
                warehousePlaceConf2,
                warehousePlaceConf3,
                warehousePlaceConf4]

    @property
    def isExecuting(self) -> bool:
        if self.__warehouseActConveyorIn or self.__warehouseActConveyorOut or self.__warehouseActHorizontalToRack or self.__warehouseActHorizontalToConveyor or self.__warehouseActVerticalUp or self.__warehouseActVerticalDown or self.__warehouseActArmIn or self.__warehouseActArmOut:
            return True
        else:
            return False

    def __init__(self, id1):
        conveyor = [1380, 40]
        box1 = [150, 1460]
        box2 = [150, 2620]
        box3 = [150, 3780]
        box4 = [850, 1460]
        box5 = [850, 2620]
        box6 = [850, 3780]
        box7 = [1630, 1460]
        box8 = [1630, 2620]
        box9 = [1630, 3780]
        super().__init__(id1, [conveyor, box1, box2, box3, box4, box5, box6, box7, box8, box9])
        self.__warehouseSensHorizontalEnd = self.__warehouseSensLightBarrierIn = self.__warehouseSensLightBarrierOut = self.__warehouseSensVerticalEnd = self.__warehouseSensArmIn = self.__warehouseSensArmOut = False
        self.__warehouseSensEncoderHorizontal = self.__warehouseSensEncoderVertical = 0
        self.__warehouseActConveyorIn = self.__warehouseActConveyorOut = self.__warehouseActHorizontalToRack = self.__warehouseActHorizontalToConveyor = self.__warehouseActVerticalUp = self.__warehouseActVerticalDown = self.__warehouseActArmIn = self.__warehouseActArmOut = False
        self.__axisVertical = Axis(AxisType.Encoder, 13)
        self.__axisHorizontal = Axis(AxisType.Encoder, 13)


    @property
    def warehouseSensHorizontalEnd(self) -> bool:
        return self.__warehouseSensHorizontalEnd

    @warehouseSensHorizontalEnd.setter
    def warehouseSensHorizontalEnd(self, value: bool):
        self.__warehouseSensHorizontalEnd = value

    @property
    def warehouseSensLightBarrierIn(self):
        return self.__warehouseSensLightBarrierIn

    @warehouseSensLightBarrierIn.setter
    def warehouseSensLightBarrierIn(self, value):
        self.__warehouseSensLightBarrierIn = value

    @property
    def warehouseSensLightBarrierOut(self):
        return self.__warehouseSensLightBarrierOut

    @warehouseSensLightBarrierOut.setter
    def warehouseSensLightBarrierOut(self, value):
        self.__warehouseSensLightBarrierOut = value

    @property
    def warehouseSensVerticalEnd(self):
        return self.__warehouseSensVerticalEnd

    @warehouseSensVerticalEnd.setter
    def warehouseSensVerticalEnd(self, value):
        self.__warehouseSensVerticalEnd = value

    @property
    def warehouseSensArmIn(self):
        return self.__warehouseSensArmIn

    @warehouseSensArmIn.setter
    def warehouseSensArmIn(self, value):
        self.__warehouseSensArmIn = value

    @property
    def warehouseSensArmOut(self):
        return self.__warehouseSensArmOut

    @warehouseSensArmOut.setter
    def warehouseSensArmOut(self, value):
        self.__warehouseSensArmOut = value

    @property
    def warehouseSensEncoderHorizontal(self):
        return self.__warehouseSensEncoderHorizontal

    @warehouseSensEncoderHorizontal.setter
    def warehouseSensEncoderHorizontal(self, value):
        self.__warehouseSensEncoderHorizontal = value

    @property
    def warehouseSensEncoderVertical(self):
        return self.__warehouseSensEncoderVertical

    @warehouseSensEncoderVertical.setter
    def warehouseSensEncoderVertical(self, value):
        self.__warehouseSensEncoderVertical = value

    @property
    def warehouseActConveyorIn(self):
        return self.__warehouseActConveyorIn

    @warehouseActConveyorIn.setter
    def warehouseActConveyorIn(self, value):
        self.__warehouseActConveyorIn = value

    @property
    def warehouseActConveyorOut(self):
        return self.__warehouseActConveyorOut

    @warehouseActConveyorOut.setter
    def warehouseActConveyorOut(self, value):
        self.__warehouseActConveyorOut = value

    @property
    def warehouseActHorizontalToRack(self):
        return self.__warehouseActHorizontalToRack

    @warehouseActHorizontalToRack.setter
    def warehouseActHorizontalToRack(self, value):
        self.__warehouseActHorizontalToRack = value

    @property
    def warehouseActHorizontalToConveyor(self):
        return self.__warehouseActHorizontalToConveyor

    @warehouseActHorizontalToConveyor.setter
    def warehouseActHorizontalToConveyor(self, value):
        self.__warehouseActHorizontalToConveyor = value

    @property
    def warehouseActVerticalDown(self):
        return self.__warehouseActVerticalDown

    @warehouseActVerticalDown.setter
    def warehouseActVerticalDown(self, value):
        self.__warehouseActVerticalDown = value

    @property
    def warehouseActVerticalUp(self):
        return self.__warehouseActVerticalUp

    @warehouseActVerticalUp.setter
    def warehouseActVerticalUp(self, value):
        self.__warehouseActVerticalUp = value

    @property
    def warehouseActArmIn(self):
        return self.__warehouseActArmIn

    @warehouseActArmIn.setter
    def warehouseActArmIn(self, value):
        self.__warehouseActArmIn = value

    @property
    def warehouseActArmOut(self):
        return self.__warehouseActArmOut

    @warehouseActArmOut.setter
    def warehouseActArmOut(self, value):
        self.__warehouseActArmOut = value

    #TODO execute-Logik

    #TODO speichermechanismus für Belegung des Regals

    def gotoConfig(self, config):
        t1 = t2 = t3 = t4 = False
        self.__axisVertical.update(self.warehouseSensVerticalEnd, self.warehouseSensEncoderVertical)
        t1 = self.__axisVertical.gotoConfig(config.verticalEnd, config.counterVertical)
        self.warehouseActVerticalUp = self.__axisVertical.outputminus
        self.warehouseActVerticalDown = self.__axisVertical.outputplus
        self.__axisHorizontal.update(self.warehouseSensHorizontalEnd, self.warehouseSensEncoderHorizontal)
        t2 = self.__axisHorizontal.gotoConfig(config.horizontalEnd, config.counterHorizontal)
        self.warehouseActHorizontalToConveyor = self.__axisHorizontal.outputminus
        self.warehouseActHorizontalToRack = self.__axisHorizontal.outputplus

        if config.armEndIn:
            if not self.warehouseSensArmIn:
                self.warehouseActArmIn = True
            else:
                self.warehouseActArmIn = False
                t3 = True
        if config.armEndOut:
            if not self.warehouseSensArmOut:
                self.warehouseActArmOut = True
            else:
                self.warehouseActArmOut = False
                t3 = True
        if config.conveyorIn:
            self.warehouseActConveyorIn = True
            if not self.warehouseSensLightBarrierIn:
                t4 = True
        else:
            self.warehouseActConveyorIn = False
        if config.conveyorOut:
            self.warehouseActConveyorOut = True
            if not self.warehouseSensLightBarrierOut:
                t4 = True
        else:
            self.warehouseActConveyorOut = False
        if not config.conveyorOut and not config.conveyorIn:
            t4 = True
        return t1 and t2 and t3 and t4

    def setup(self):
        t1 = t2 = t3 = False
        if self.warehouseSensArmIn:
            self.warehouseActArmIn = False
            t1 = True
        else:
            self.warehouseActArmIn = True

        if self.warehouseSensVerticalEnd:
            self.warehouseActVerticalUp = False
            t2 = True
        elif t1: #only move after arm is in secure position
            self.warehouseActVerticalUp = True

        if self.warehouseSensHorizontalEnd:
            self.warehouseActHorizontalToConveyor = False
            t3 = True
        elif t1:
            self.warehouseActHorizontalToConveyor = True

        return (t1 and t2 and t3)

    def executeHelper(self):
        """Used to manage reset of encoder counters end of setup

        :return: bool, bool: flag to allow reset
        """
        if self.setupFinishedHelper:
            self.setupFinishedHelper = False
            return True, True
        else:
            return False, False

