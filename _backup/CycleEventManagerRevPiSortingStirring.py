#!/usr/bin/env python

import revpimodio2
from Robot import Robot
from Warehouse import Warehouse
from Conveyor import Conveyor
from ThreeDRobotConfig import ThreeDRobotConfig
from VacuumGripper import VacuumGripper
from SortingLine import SortingLine
from DummyMachine import DummyMachine
from SequenceManager import SequenceManager
from IndexedLine import IndexedLine


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

        #vertical, rot, arm
        pickupRobot1 = [2600,3550,25]
        placeConveyorRobot1 = [2000,100,79]
        placeListrobot1 = [pickupRobot1, placeConveyorRobot1]

        warehouseRobot2 = [300,1432,1950]
        sortingWhiteRobot2 = [1500,3010,1600]
        sortingBlueRobot2 = [1500,2760,1085]
        sortingRedRobot2 = [1500,2890,1220]
        indexedLineRobot2 = [1200,2230,900]
        placeListrobot2 = [warehouseRobot2,sortingWhiteRobot2,sortingBlueRobot2,sortingRedRobot2,indexedLineRobot2]

        indexedLineRobot3 = [2100,2940,65]
        placeConveyorRobot3 = [1600,4050,5]
        placeExtRobot3 = [1,1,1]
        placeListrobot3 = [indexedLineRobot3, placeConveyorRobot3, placeExtRobot3]

        self.robot1 = Robot(1, placeListrobot1)
        self.conveyor1 = Conveyor(2)
        self.sortingLine1 = SortingLine(3)
        self.vacuum1 = VacuumGripper(4, placeListrobot2)
        self.warehouse1 = Warehouse(5)
        self.indexedLine = IndexedLine(6)
        self.robot2 = Robot(7, placeListrobot3)
        self.conveyor2 = Conveyor(8)
        self.sortingstirringSequence = SequenceManager(1, self.robot1,
                                                       self.conveyor1,
                                                       self.sortingLine1,
                                                       self.vacuum1,
                                                       self.warehouse1,
                                                       self.indexedLine,
                                                       self.robot2,
                                                       self.conveyor2)

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
        self.rpi.io.dio3_O_1.value = False
        self.rpi.io.dio3_O_2.value = False
        self.rpi.io.dio3_O_3.value = False
        self.rpi.io.dio3_O_4.value = False
        self.rpi.io.dio3_O_5.value = False
        self.rpi.io.dio3_O_6.value = False
        self.rpi.io.dio3_O_7.value = False
        self.rpi.io.dio3_O_8.value = False
        self.rpi.io.dio3_O_9.value = False
        self.rpi.io.dio3_O_10.value = False
        self.rpi.io.dio3_O_11.value = False
        self.rpi.io.dio3_O_12.value = False
        self.rpi.io.dio3_O_13.value = False
        self.rpi.io.dio3_O_14.value = False
        self.rpi.io.dio4_O_1.value = False
        self.rpi.io.dio4_O_2.value = False
        self.rpi.io.dio4_O_3.value = False
        self.rpi.io.dio4_O_4.value = False
        self.rpi.io.dio4_O_5.value = False
        self.rpi.io.dio4_O_6.value = False
        self.rpi.io.dio4_O_7.value = False
        self.rpi.io.dio4_O_8.value = False
        self.rpi.io.dio4_O_9.value = False
        self.rpi.io.dio4_O_10.value = False
        self.rpi.io.dio4_O_11.value = False
        self.rpi.io.dio4_O_12.value = False
        self.rpi.io.dio4_O_13.value = False
        self.rpi.io.dio4_O_14.value = False
        self.rpi.io.dio5_O_1.value = False
        self.rpi.io.dio5_O_2.value = False
        self.rpi.io.dio5_O_3.value = False
        self.rpi.io.dio5_O_4.value = False
        self.rpi.io.dio5_O_5.value = False
        self.rpi.io.dio5_O_6.value = False
        self.rpi.io.dio5_O_7.value = False
        self.rpi.io.dio5_O_8.value = False
        self.rpi.io.dio5_O_9.value = False
        self.rpi.io.dio5_O_10.value = False
        self.rpi.io.dio5_O_11.value = False
        self.rpi.io.dio5_O_12.value = False
        self.rpi.io.dio5_O_13.value = False
        self.rpi.io.dio5_O_14.value = False

    def start(self):
        """Start event system and own cyclic loop."""

        # Start event system without blocking here
        self.rpi.mainloop(blocking=False)

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        while not self.rpi.exitsignal.wait(0.03):
            # Switch on / off green part of LED A1 | or do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            # READ   READ   READ   READ
            self.read()

            # NEW

            #TheSortingSequence
            #self.indexedLine.processPackage()
            self.sortingstirringSequence.executeSortingStirring()

            # EXECUTE   EXECUTE   EXECUTE    EXECUTE
            #self.sortingLine1.execute()
            #self.conveyor1.execute()
            #self.robot1.execute(0,1)
            #self.warehouse1.execute(0,1)
            #self.vacuum1.execute(4,0)
            #
            # HELPER   HELPER   HELPER    HELPER
            flagEncoderHorizontal, flagEncoderVertical = self.warehouse1.executeHelper()
            flagEncoderRot, flagEncoderVertical2 = self.robot1.executeHelper()
            flagEncoder1, flagEncoder2, flagEncoder3 = self.vacuum1.executeHelper()
            flagEncoderRot3, flagEncoderVertical3 = self.robot2.executeHelper()

            # WRITE   WRITE   WRITE   WRITE
            self.write()

            # RESET   RESET   RESET   RESET

            self.reset(flagEncoderHorizontal, flagEncoderVertical)
            self.reset1(flagEncoderRot, flagEncoderVertical2)
            self.reset2(flagEncoder1, flagEncoder2, flagEncoder3)
            self.reset3(flagEncoderRot3, flagEncoderVertical3)

        

    def read(self):

        #warehouse
        self.warehouse1.warehouseSensHorizontalEnd = self.rpi.io.dio2_I_7.value
        self.warehouse1.warehouseSensLightBarrierIn = self.rpi.io.dio2_I_8.value
        self.warehouse1.warehouseSensLightBarrierOut = self.rpi.io.dio2_I_9.value
        self.warehouse1.warehouseSensVerticalEnd = self.rpi.io.dio2_I_10.value
        self.warehouse1.warehouseSensEncoderHorizontal = self.rpi.io.dio2_Counter_11.value
        self.warehouse1.warehouseSensEncoderVertical = self.rpi.io.dio2_Counter_13.value
        self.warehouse1.warehouseSensArmOut = self.rpi.io.dio3_I_1.value
        self.warehouse1.warehouseSensArmIn = self.rpi.io.dio3_I_2.value
        #sortingLine
        self.sortingLine1.sortingLineSensImpulseCounterRaw = self.rpi.io.dio2_Counter_1.value
        self.sortingLine1.sortingLineSensInputLightBarrier = self.rpi.io.dio2_I_2.value
        self.sortingLine1.sortingLineSensMiddleLightBarrier = self.rpi.io.dio2_I_3.value
        self.sortingLine1.sortingLineSensWhiteLightBarrier = self.rpi.io.dio2_I_4.value
        self.sortingLine1.sortingLineSensRedLightBarrier = self.rpi.io.dio2_I_5.value
        self.sortingLine1.sortingLineSensBlueLightBarrier = self.rpi.io.dio2_I_6.value
        #conveyor - Anfang
        self.conveyor1.conveyorSensLeft = self.rpi.io.dio1_I_11.value
        self.conveyor1.conveyorSensRight = self.rpi.io.dio1_I_12.value
        self.conveyor1.conveyorSensImpulse = self.rpi.io.dio1_Counter_13.value

        #3DRobot - Anfang
        self.robot1.robotSensGripperOpen = self.rpi.io.dio1_I_1.value
        self.robot1.robotSensGripperImpulseCounterRaw = self.rpi.io.dio1_Counter_2.value
        self.robot1.robotSensArmEndIn = self.rpi.io.dio1_I_3.value
        self.robot1.robotSensArmImpulseCounterRaw = self.rpi.io.dio1_Counter_4.value
        print(self.robot1.robotSensArmImpulseCounterRaw)
        self.robot1.robotSensVerticalEndUp = self.rpi.io.dio1_I_5.value
        self.robot1.robotSensRotEnd = self.rpi.io.dio1_I_6.value
        self.robot1.robotSensVerticalEncoderCounter = self.rpi.io.dio1_Counter_7.value
        self.robot1.robotSensRotEncoderCounter = self.rpi.io.dio1_Counter_9.value

        #VacuumGripper
        self.vacuum1.vacuumSensVerticalEndUp = self.rpi.io.dio3_I_3.value
        self.vacuum1.vacuumSensArmEndIn = self.rpi.io.dio3_I_4.value
        self.vacuum1.vacuumSensRotEnd = self.rpi.io.dio3_I_5.value
        self.vacuum1.vacuumSensVerticalEncoderCounter = self.rpi.io.dio3_Counter_7.value
        self.vacuum1.vacuumSensArmEncoderCounter = self.rpi.io.dio3_Counter_9.value
        self.vacuum1.vacuumSensRotEncoderCounter = self.rpi.io.dio3_Counter_11.value
        #conveyor - Ende
        self.conveyor2.conveyorSensLeft = self.rpi.io.dio3_I_13.value
        self.conveyor2.conveyorSensRight = self.rpi.io.dio3_I_14.value
        self.conveyor2.conveyorSensImpulse = self.rpi.io.dio3_Counter_6.value
        #indexedLine
        #Warning: backward and forward slider are swapped on the sheet.
        self.indexedLine.pushButton1Front = self.rpi.io.dio4_I_1.value
        self.indexedLine.pushButton1Back = self.rpi.io.dio4_I_2.value
        self.indexedLine.pushButton2Front = self.rpi.io.dio4_I_3.value
        self.indexedLine.pushButton2Back = self.rpi.io.dio4_I_4.value

        self.indexedLine.indexSensSlider1 = self.rpi.io.dio4_I_5.value
        self.indexedLine.indexSensMilling = self.rpi.io.dio4_I_6.value
        self.indexedLine.indexSensLoading = self.rpi.io.dio4_I_7.value
        self.indexedLine.indexSensDrilling = self.rpi.io.dio4_I_8.value
        self.indexedLine.indexSensConveyorSwap = self.rpi.io.dio4_I_9.value
        #3DRobot - Ende
        self.robot2.robotSensGripperOpen = self.rpi.io.dio5_I_1.value
        self.robot2.robotSensGripperImpulseCounterRaw = self.rpi.io.dio5_Counter_2.value
        self.robot2.robotSensArmEndIn = self.rpi.io.dio5_I_3.value
        self.robot2.robotSensArmImpulseCounterRaw = self.rpi.io.dio5_Counter_4.value
        #print(self.robot2.robotSensArmImpulseCounterRaw)
        self.robot2.robotSensVerticalEndUp = self.rpi.io.dio5_I_5.value
        self.robot2.robotSensRotEnd = self.rpi.io.dio5_I_6.value
        self.robot2.robotSensVerticalEncoderCounter = self.rpi.io.dio5_Counter_7.value
        self.robot2.robotSensRotEncoderCounter = self.rpi.io.dio5_Counter_9.value


    def write(self):

        #warehouse
        self.rpi.io.dio2_O_7.value = self.warehouse1.warehouseActConveyorOut
        self.rpi.io.dio2_O_8.value = self.warehouse1.warehouseActConveyorIn
        self.rpi.io.dio2_O_9.value = self.warehouse1.warehouseActHorizontalToRack
        self.rpi.io.dio2_O_10.value = self.warehouse1.warehouseActHorizontalToConveyor
        self.rpi.io.dio2_O_11.value = self.warehouse1.warehouseActVerticalDown
        self.rpi.io.dio2_O_12.value = self.warehouse1.warehouseActVerticalUp
        self.rpi.io.dio2_O_13.value = self.warehouse1.warehouseActArmOut
        self.rpi.io.dio2_O_14.value = self.warehouse1.warehouseActArmIn
        #sortingLine
        self.rpi.io.dio2_O_1.value = self.sortingLine1.sortingLineActMotorConveyor
        self.rpi.io.dio2_O_2.value = self.sortingLine1.sortingLineActCompressorOn
        self.rpi.io.dio2_O_3.value = self.sortingLine1.sortingLineActWhiteEjector
        self.rpi.io.dio2_O_4.value = self.sortingLine1.sortingLineActRedEjector
        self.rpi.io.dio2_O_5.value = self.sortingLine1.sortingLineActBlueEjector
        #conveyor
        self.rpi.io.dio1_O_9.value = self.conveyor1.conveyorActForward
        self.rpi.io.dio1_O_10.value = self.conveyor1.conveyorActBackward

        #3DRobot - Anfang
        self.rpi.io.dio1_O_1.value = self.robot1.robotActGripperOpen
        self.rpi.io.dio1_O_2.value = self.robot1.robotActGripperClose
        self.rpi.io.dio1_O_3.value = self.robot1.robotActArmOut
        self.rpi.io.dio1_O_4.value = self.robot1.robotActArmIn
        self.rpi.io.dio1_O_5.value = self.robot1.robotActVerticalDown
        self.rpi.io.dio1_O_6.value = self.robot1.robotActVerticalUp
        self.rpi.io.dio1_O_7.value = self.robot1.robotActRotRight
        self.rpi.io.dio1_O_8.value = self.robot1.robotActRotLeft

        #VacuumGripper
        self.rpi.io.dio3_O_1.value = self.vacuum1.vacuumActVerticalUp
        self.rpi.io.dio3_O_2.value = self.vacuum1.vacuumActVerticalDown
        self.rpi.io.dio3_O_3.value = self.vacuum1.vacuumActArmIn
        self.rpi.io.dio3_O_4.value = self.vacuum1.vacuumActArmOut
        self.rpi.io.dio3_O_5.value = self.vacuum1.vacuumActRotRight
        self.rpi.io.dio3_O_6.value = self.vacuum1.vacuumActRotLeft
        self.rpi.io.dio3_O_7.value = self.vacuum1.vacuumActCompressorOn
        self.rpi.io.dio3_O_8.value = self.vacuum1.vacuumActValve
        #conveyor - Ende
        self.rpi.io.dio3_O_9.value = self.conveyor2.conveyorActForward
        self.rpi.io.dio3_O_10.value = self.conveyor2.conveyorActBackward
        #indexedLine
        self.rpi.io.dio4_O_2.value = self.indexedLine.motorSlider1Backward
        self.rpi.io.dio4_O_1.value = self.indexedLine.motorSlider1Forward
        self.rpi.io.dio4_O_4.value = self.indexedLine.motorSlider2Backward
        self.rpi.io.dio4_O_3.value = self.indexedLine.motorSlider2Forward
        self.rpi.io.dio4_O_5.value = self.indexedLine.conveyorBeltFeed
        self.rpi.io.dio4_O_6.value = self.indexedLine.conveyorBeltMilling
        self.rpi.io.dio4_O_7.value = self.indexedLine.millingMachine
        self.rpi.io.dio4_O_8.value = self.indexedLine.conveyorBeltDrilling
        self.rpi.io.dio4_O_9.value = self.indexedLine.drillingMachine
        self.rpi.io.dio4_O_10.value = self.indexedLine.conveyorBeltSwap
        #3DRobot - Ende
        self.rpi.io.dio5_O_1.value = self.robot2.robotActGripperOpen
        self.rpi.io.dio5_O_2.value = self.robot2.robotActGripperClose
        self.rpi.io.dio5_O_3.value = self.robot2.robotActArmOut
        self.rpi.io.dio5_O_4.value = self.robot2.robotActArmIn
        self.rpi.io.dio5_O_5.value = self.robot2.robotActVerticalDown
        self.rpi.io.dio5_O_6.value = self.robot2.robotActVerticalUp
        self.rpi.io.dio5_O_7.value = self.robot2.robotActRotRight
        self.rpi.io.dio5_O_8.value = self.robot2.robotActRotLeft


    def reset(self, flagEncoderHorizontal, flagEncoderVertical):
        if flagEncoderHorizontal:
            self.rpi.io.dio2_Counter_11.reset()
            #print("resetHorizontal")
        if flagEncoderVertical:
            self.rpi.io.dio2_Counter_13.reset()
            #print("resetVertical")

    def reset1(self, flagEncoderRot, flagEncoderVertical):
        if flagEncoderRot:
            self.rpi.io.dio1_Counter_9.reset()
        if flagEncoderVertical:
            self.rpi.io.dio1_Counter_7.reset()

    def reset2(self, flagEncoder1, flagEncoder2, flagEncoder3):
        if flagEncoder1:
            self.rpi.io.dio3_Counter_11.reset()
            self.rpi.io.dio3_Counter_9.reset()
            self.rpi.io.dio3_Counter_7.reset()

    def reset3(self, flagEncoderRot3, flagEncoderVertical3):
        if flagEncoderRot3:
            self.rpi.io.dio5_Counter_7.reset()
            self.rpi.io.dio5_Counter_9.reset()


if __name__ == "__main__":
    # Start RevPiApp app
    root = CycleEventManagerRevPiTestSetup()
    root.start()
