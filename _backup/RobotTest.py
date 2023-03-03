import unittest

from Robot import Robot
from ThreeDRobotConfig import ThreeDRobotConfig
from PlusMinusStop import PlusMinusStop


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pickupRobot1 = [2600,3550,25]
        placeConveyorRobot1 = [2000,100,100]
        placeListrobot1 = [pickupRobot1, placeConveyorRobot1]
        self.robot1 = Robot(1, placeListrobot1)

    def testExecute(self):
        # SETUP
        self.robot1.robotSensRotEnd = True
        self.robot1.robotSensArmEndIn = True
        self.robot1.robotSensGripperOpen = True
        self.robot1.robotSensVerticalEndUp = True
        #setup finished, pc = 0
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.setupFinishedHelper, True)
        self.assertEqual(self.robot1.pc, 0)
        # PICK
        #first two configs already reached coming from setup
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.pc, 1)
        self.robot1.execute(0,1)
        self.robot1.execute(0,1)
        #this config is not reached yet
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, True)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, True)
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, True)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, True)
        self.robot1.robotSensRotEncoderCounter = 3550
        self.robot1.robotSensVerticalEncoderCounter = 1900
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.robot1.robotSensArmImpulseCounterRaw = 0
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, True)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.robot1.robotSensArmImpulseCounterRaw = 1
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, True)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.robot1.robotSensArmImpulseCounterRaw = 25
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, True)
        self.robot1.robotSensVerticalEncoderCounter = 2600
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.assertEqual(self.robot1.robotActGripperClose, False)
        self.robot1.robotSensGripperImpulseCounterRaw = 0
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.assertEqual(self.robot1.robotActGripperClose, True)
        self.robot1.robotSensGripperImpulseCounterRaw = 1
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.assertEqual(self.robot1.robotActGripperClose, True)
        self.robot1.robotSensGripperImpulseCounterRaw = 14
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalDown, False)
        self.assertEqual(self.robot1.robotActGripperClose, False)
        self.robot1.robotSensGripperImpulseCounterRaw = 1
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalUp, True)
        self.assertEqual(self.robot1.robotActGripperClose, False)
        self.robot1.robotSensVerticalEncoderCounter = 1900
        self.robot1.execute(0,1)
        self.assertEqual(self.robot1.robotActRotLeft, False)
        self.assertEqual(self.robot1.robotActArmOut, False)
        self.assertEqual(self.robot1.robotActVerticalUp, False)
        self.assertEqual(self.robot1.robotActGripperClose, False)
        # PLACE


if __name__ == '__main__':
    unittest.main()
