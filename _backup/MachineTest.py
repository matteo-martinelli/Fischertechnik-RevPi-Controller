import unittest
#from time import time
from time import sleep
from Machine import Machine


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.machine1 = Machine(1)

    def testTimeSinceExecution(self):
        self.machine1.isExecuting = True
        self.assertEqual(self.machine1.timeSinceExecution(), 0)
        self.machine1.isExecuting = False
        sleep(2)
        self.assertAlmostEqual(self.machine1.timeSinceExecution(), 2, 1)
        self.machine1.isExecuting = True
        self.assertEqual(self.machine1.timeSinceExecution(), 0)

if __name__ == '__main__':
    unittest.main()
