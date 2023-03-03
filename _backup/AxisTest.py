import unittest

from DeleteAfterTests import RobotTester
from Axis import Axis, AxisType


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.robot = RobotTester(1)
        self.axis = Axis(AxisType.Counter, 1)

    def testUpdate(self):
        self.assertEqual(self.axis.counterinput, 0)
        self.robot.robotSensArmImpulseCounterRaw = 10
        self.axis.update(self.robot.robotSensArmEndIn, self.robot.robotSensArmImpulseCounterRaw)
        self.assertEqual(self.axis.counterinput, 10)

    def testCounter(self):
        pass

if __name__ == '__main__':
    unittest.main()
