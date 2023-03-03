#!/usr/bin/env python

import revpimodio2
from Robot import Robot
from ThreeDRobotConfig import ThreeDRobotConfig
from PunchingMachine import PunchingMachine


class CycleEventManagerRevPi():

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

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""

        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False
        self.rpi.io.O_1.value = False
        self.rpi.io.O_2.value = False
        self.rpi.io.O_3.value = False
        self.rpi.io.O_4.value = False
        self.rpi.io.O_5.value = False
        self.rpi.io.O_6.value = False
        self.rpi.io.O_7.value = False
        self.rpi.io.O_8.value = False

    def event_flipflop_o1(self, ioname, iovalue):
        """Called if I_1 goes to True."""

        # Switch on/off output O_1
        self.rpi.io.O_1.value = not self.rpi.io.O_1.value

    def start(self):
        """Start event system and own cyclic loop."""

        # Start event system without blocking here
        self.rpi.mainloop(blocking=False)

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        while not self.rpi.exitsignal.wait(0.05):

            # Switch on / off green part of LED A1 | or do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            self.read()
            self.robot1.execute()
            #lagEncoderRot, flagEncoderVertical = self.robot1.executeHelper()
            self.write()
            self.reset(flagEncoderRot, flagEncoderVertical)

    def read(self):
        self.robot1.robotSensGripperOpen = self.rpi.io.I_1.value
        self.robot1.robotSensGripperImpulseCounterRaw = self.rpi.io.Counter_2.value
        self.robot1.robotSensArmEndIn = self.rpi.io.I_3.value
        self.robot1.robotSensArmImpulseCounterRaw = self.rpi.io.Counter_4.value
        self.robot1.robotSensVerticalEndUp = self.rpi.io.I_5.value
        self.robot1.robotSensRotEnd = self.rpi.io.I_6.value
        self.robot1.robotSensVerticalEncoderCounter = self.rpi.io.Counter_7.value
        print(self.robot1.robotSensVerticalEncoderCounter)
        self.robot1.robotSensRotEncoderCounter = self.rpi.io.Counter_9.value
        #print(self.robot1.robotSensRotEncoderCounter)

    def write(self):
        self.rpi.io.O_1.value = self.robot1.robotActGripperOpen
        self.rpi.io.O_2.value = self.robot1.robotActGripperClose
        self.rpi.io.O_3.value = self.robot1.robotActArmOut
        self.rpi.io.O_4.value = self.robot1.robotActArmIn
        self.rpi.io.O_5.value = self.robot1.robotActVerticalDown
        self.rpi.io.O_6.value = self.robot1.robotActVerticalUp
        self.rpi.io.O_7.value = self.robot1.robotActRotRight
        self.rpi.io.O_8.value = self.robot1.robotActRotLeft

    def reset(self, flagEncoderRot, flagEncoderVertical):
        if flagEncoderRot:
            self.rpi.io.Counter_9.reset()
            print("resetRot")
        if flagEncoderVertical:
            self.rpi.io.Counter_7.reset()
            print("resetVertical")


if __name__ == "__main__":
    # Start RevPiApp app
    root = CycleEventManagerRevPi()
    root.start()
