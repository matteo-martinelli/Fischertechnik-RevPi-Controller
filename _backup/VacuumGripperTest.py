import unittest

from VacuumGripper import VacuumGripper
from VacuumGripperConfig import VacuumGripperConfig
from PlusMinusStop import PlusMinusStop


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.vacuum1 = VacuumGripper(1)

    def testSetup(self):
        test = self.vacuum1.setup()
        self.assertEqual(self.vacuum1.vacuumActArmIn, True)
        test = self.vacuum1.setup()
        self.assertEqual(self.vacuum1.vacuumActArmIn, True)
        self.vacuum1.vacuumSensArmEndIn = True
        test = self.vacuum1.setup()
        self.assertEqual(self.vacuum1.vacuumActArmIn, False)
        self.assertEqual(self.vacuum1.vacuumActRotRight, True)


    if __name__ == '__main__':
        unittest.main()
