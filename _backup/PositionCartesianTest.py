import unittest

from PositionCartesian import PositionCartesian

class PositionCartesianTest(unittest.TestCase):
    def setUp(self):
        self.pos = PositionCartesian(10,20,20)

    def testDist(self):
        self.assertEqual(self.pos.distFrom(10,20,10), 10)

if __name__ == '__main__':
    unittest.main()
