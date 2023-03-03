import unittest

from SortingLine import SortingLine
from Colour import Colour


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sorting1 = SortingLine(1)

    def testEjectBlue(self):
        self.sorting1.sortingLineSensImpulseCounterRaw = 200
        #compute
        self.sorting1.ejectColour(Colour.BLUE)
        #self.assertEqual(self.sorting1.sortingLineActMotorConveyor, False)
        self.sorting1.sortingLineSensInputLightBarrier = False
        #compute
        self.sorting1.ejectColour(Colour.BLUE)
        self.assertEqual(self.sorting1.isExecuting, True)
        self.assertEqual(self.sorting1.sortingLineActMotorConveyor, True)
        self.sorting1.sortingLineSensImpulseCounterRaw = 400
        #compute
        self.sorting1.ejectColour(Colour.BLUE)
        self.assertEqual(self.sorting1.sortingLineActMotorConveyor, True)
        self.sorting1.sortingLineSensMiddleLightBarrier = False
        self.sorting1.sortingLineSensImpulseCounterRaw = 450
        #compute - ab hier muss mitgezählt werden
        self.sorting1.ejectColour(Colour.BLUE)
        self.assertEqual(self.sorting1.sortingLineActMotorConveyor, True)
        self.assertEqual(self.sorting1.sortingLineCounterValue, 50)
        self.sorting1.sortingLineSensImpulseCounterRaw = 505
        #compute
        self.sorting1.ejectColour(Colour.BLUE)
        self.assertEqual(self.sorting1.sortingLineActMotorConveyor, False)
        self.assertEqual(self.sorting1.sortingLineActCompressorOn, True)
        self.assertEqual(self.sorting1.sortingLineActBlueEjector,True)

if __name__ == '__main__':
    unittest.main()
