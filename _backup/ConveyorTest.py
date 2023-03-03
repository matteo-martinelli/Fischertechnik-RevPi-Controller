import unittest

from IllegalValueCombination import IllegalValueCombination
from Conveyor import Conveyor


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.conveyor1 = Conveyor(1)

    def testSetAct(self):
        self.assertEqual(self.conveyor1.id, 1)
        self.conveyor1.conveyorActForward = True
        self.assertEqual(self.conveyor1.conveyorActForward, True)
        with self.assertRaises(IllegalValueCombination):
            self.conveyor1.conveyorActBackward = True
        self.conveyor1.conveyorActForward = False
        self.conveyor1.conveyorActBackward = True
        #TODO how to avoid following action?
        self.conveyor1.conveyorActForward = 10

if __name__ == '__main__':
    unittest.main()
