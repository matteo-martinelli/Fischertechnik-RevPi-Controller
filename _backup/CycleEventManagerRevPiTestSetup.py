#!/usr/bin/env python

import revpimodio2
from Robot import Robot
from Warehouse import Warehouse
from ThreeDRobotConfig import ThreeDRobotConfig
from VacuumGripper import VacuumGripper
from SortingLine import SortingLine


class CycleEventManagerRevPiTestSetup():

    """Mainapp for RevPi."""

    def __init__(self):
        """Init MyRevPiApp class."""

        # Instantiate RevPiModIO
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)

        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)

        # Register event to toggle output O_1 with input I_1
        #self.rpi.io.I_1.reg_event(self.event_flipflop_o1, edge=revpimodio2.RISING)

        #create objects
        config1 = ThreeDRobotConfig(2800,350,0,0,False,False,False,False)
        config2 = ThreeDRobotConfig(2800,350,0,23,False,False,False,False)
        config3 = ThreeDRobotConfig(100,350,0,23,False,False,False,False)
        config4 = ThreeDRobotConfig(100,3350,25,23,False,False,False,False)
        config5 = ThreeDRobotConfig(2300,3350,25,23,False,False,False,False)
        config6 = ThreeDRobotConfig(2300,3350,25,0,False,False,False,True)
        confList = [config1, config2, config3, config4,config5,config6]
        self.robot1 = Robot(1, confList)
        self.vacuum1 = VacuumGripper(1)
        self.warehouse1 = Warehouse(1)
        self.sortingLine1 = SortingLine(1)

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""

        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False
        self.rpi.io.dio1_O_1.value = False
        self.rpi.io.dio1_O_2.value = False
        self.rpi.io.dio1_O_3.value = False
        self.rpi.io.dio1_O_4.value = False
        self.rpi.io.dio1_O_5.value = False
        self.rpi.io.dio1_O_6.value = False
        self.rpi.io.dio1_O_7.value = False
        self.rpi.io.dio1_O_8.value = False
        self.rpi.io.dio1_O_9.value = False
        self.rpi.io.dio1_O_10.value = False
        self.rpi.io.dio1_O_11.value = False
        self.rpi.io.dio1_O_12.value = False
        self.rpi.io.dio1_O_13.value = False
        self.rpi.io.dio1_O_14.value = False
        self.rpi.io.dio2_O_1.value = False
        self.rpi.io.dio2_O_2.value = False
        self.rpi.io.dio2_O_3.value = False
        self.rpi.io.dio2_O_4.value = False
        self.rpi.io.dio2_O_5.value = False
        self.rpi.io.dio2_O_6.value = False
        self.rpi.io.dio2_O_7.value = False
        self.rpi.io.dio2_O_8.value = False
        self.rpi.io.dio2_O_9.value = False
        self.rpi.io.dio2_O_10.value = False
        self.rpi.io.dio2_O_11.value = False
        self.rpi.io.dio2_O_12.value = False
        self.rpi.io.dio2_O_13.value = False
        self.rpi.io.dio2_O_14.value = False

    def start(self):
        """Start event system and own cyclic loop."""

        # Start event system without blocking here
        self.rpi.mainloop(blocking=False)

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        while not self.rpi.exitsignal.wait(0.01):

            # Switch on / off green part of LED A1 | or do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value
            self.read()
            #self.robot1.execute()
            #self.warehouse1.execute()
            #flagEncoderHorizontal, flagEncoderVertical = self.warehouse1.executeHelper()
            self.sortingLine1.execute()
            self.vacuum1.execute()
            flagEncoder1, flagEncoder2, flagEncoder3 = self.vacuum1.executeHelper()
            self.write()

            #self.reset(flagEncoderHorizontal, flagEncoderVertical)
            self.reset2(flagEncoder1, flagEncoder2, flagEncoder3)

    def read(self):
        self.vacuum1.vacuumSensVerticalEndUp = self.rpi.io.dio1_I_8.value
        #print("verticalEndUp")
        #print(self.vacuum1.vacuumSensVerticalEndUp)
        self.vacuum1.vacuumSensArmEndIn = self.rpi.io.dio1_I_9.value
        #print("ArmEnd")
        #print(self.vacuum1.vacuumSensArmEndIn)
        self.vacuum1.vacuumSensRotEnd = self.rpi.io.dio1_I_10.value
        #print("RotEnd")
        #print(self.vacuum1.vacuumSensRotEnd)
        self.vacuum1.vacuumSensVerticalEncoderCounter = self.rpi.io.dio1_Counter_11.value
        self.vacuum1.vacuumSensArmEncoderCounter = self.rpi.io.dio1_Counter_13.value
        self.vacuum1.vacuumSensRotEncoderCounter = self.rpi.io.dio2_Counter_1.value
        ####################
        ####################
        """
        self.warehouse1.warehouseSensHorizontalEnd = self.rpi.io.dio2_I_3.value
        self.warehouse1.warehouseSensLightBarrierIn = self.rpi.io.dio2_I_4.value
        self.warehouse1.warehouseSensLightBarrierOut = self.rpi.io.dio2_I_5.value
        self.warehouse1.warehouseSensVerticalEnd = self.rpi.io.dio2_I_6.value
        self.warehouse1.warehouseSensEncoderHorizontal = self.rpi.io.dio2_Counter_7.value
        self.warehouse1.warehouseSensEncoderVertical = self.rpi.io.dio2_Counter_9.value
        self.warehouse1.warehouseSensArmOut = self.rpi.io.dio2_I_11.value
        self.warehouse1.warehouseSensArmIn = self.rpi.io.dio2_I_12.value
        """
        self.sortingLine1.sortingLineSensImpulseCounterRaw = self.rpi.io.dio2_Counter_5.value
        self.sortingLine1.sortingLineSensInputLightBarrier = self.rpi.io.dio2_I_6.value
        self.sortingLine1.sortingLineSensMiddleLightBarrier = self.rpi.io.dio2_I_7.value
        self.sortingLine1.sortingLineSensWhiteLightBarrier = self.rpi.io.dio2_I_8.value
        self.sortingLine1.sortingLineSensRedLightBarrier = self.rpi.io.dio2_I_9.value
        self.sortingLine1.sortingLineSensBlueLightBarrier = self.rpi.io.dio2_I_10.value



    def write(self):
        self.rpi.io.dio1_O_7.value = self.vacuum1.vacuumActVerticalUp
        self.rpi.io.dio1_O_8.value = self.vacuum1.vacuumActVerticalDown
        self.rpi.io.dio1_O_9.value = self.vacuum1.vacuumActArmIn
        self.rpi.io.dio1_O_10.value = self.vacuum1.vacuumActArmOut
        self.rpi.io.dio1_O_11.value = self.vacuum1.vacuumActRotRight
        self.rpi.io.dio1_O_12.value = self.vacuum1.vacuumActRotLeft
        self.rpi.io.dio1_O_13.value = self.vacuum1.vacuumActCompressorOn
        self.rpi.io.dio1_O_14.value = self.vacuum1.vacuumActValve
        #self.rpi.io.dio2_O_1.value = self.warehouse1.warehouseActConveyorOut
        #self.rpi.io.dio2_O_2.value = self.warehouse1.warehouseActConveyorIn
        #self.rpi.io.dio2_O_3.value = self.warehouse1.warehouseActHorizontalToRack
        #self.rpi.io.dio2_O_4.value = self.warehouse1.warehouseActHorizontalToConveyor
        #self.rpi.io.dio2_O_5.value = self.warehouse1.warehouseActVerticalDown
        #self.rpi.io.dio2_O_6.value = self.warehouse1.warehouseActVerticalUp
        #self.rpi.io.dio2_O_7.value = self.warehouse1.warehouseActArmOut
        #self.rpi.io.dio2_O_8.value = self.warehouse1.warehouseActArmIn
        #print("ArmInAct")
        #print(self.warehouse1.warehouseActArmIn)
        self.rpi.io.dio2_O_1.value = self.sortingLine1.sortingLineActMotorConveyor
        self.rpi.io.dio2_O_2.value = self.sortingLine1.sortingLineActCompressorOn
        self.rpi.io.dio2_O_3.value = self.sortingLine1.sortingLineActWhiteEjector
        self.rpi.io.dio2_O_4.value = self.sortingLine1.sortingLineActRedEjector
        self.rpi.io.dio2_O_5.value = self.sortingLine1.sortingLineActBlueEjector

    def reset(self, flagEncoderRot, flagEncoderVertical):
        if flagEncoderRot:
            self.rpi.io.dio2_Counter_9.reset()
            print("resetRot")
        if flagEncoderVertical:
            self.rpi.io.dio2_Counter_7.reset()
            print("resetVertical")

    def reset2(self, flagEncoder1, flagEncoder2, flagEncoder3):
        if flagEncoder1:
            self.rpi.io.dio1_Counter_11.reset()
            self.rpi.io.dio1_Counter_13.reset()
            self.rpi.io.dio2_Counter_1.reset()


if __name__ == "__main__":
    # Start RevPiApp app
    root = CycleEventManagerRevPiTestSetup()
    root.start()
