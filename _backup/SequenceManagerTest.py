import unittest

from DummyMachine import DummyMachine
from SequenceManager import SequenceManager


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.robot1 = DummyMachine(1)
        self.robot2 = DummyMachine(2)
        self.robot3 = DummyMachine(3)
        self.robot4 = DummyMachine(4)
        self.robot5 = DummyMachine(5)
        self.robot6 = DummyMachine(6)
        self.robot7 = DummyMachine(7)
        self.robot8 = DummyMachine(8)
        self.s = SequenceManager(1, self.robot1, self.robot2, self.robot3, self.robot4, self.robot5, self.robot6, self.robot7, self.robot8)

    def testInOrderExecutor(self):
        l = []
        self.s.inOrderExecutor(self.s.stationList[0:2], l)
        self.s.inOrderExecutor(self.s.stationList[0:2], l)
        self.assertEqual(l[0], True)
        self.s.inOrderExecutor(self.s.stationList[0:2], l)
        self.assertEqual(l[0], False)
        self.assertEqual(l[1], True)
        self.s.inOrderExecutor(self.s.stationList[0:2], l)
        self.assertEqual(l[0], False)
        self.assertEqual(l[1], False)
        self.assertEqual(l[2], True)
        self.s.inOrderExecutor(self.s.stationList[0:2], l)
        self.assertEqual(l[0], False)
        self.assertEqual(l[1], False)
        self.assertEqual(l[2], False)
        self.s.inOrderExecutor(self.s.stationList[0:2], l)
        self.assertEqual(l[0], True)
        self.assertEqual(l[1], False)
        self.assertEqual(l[2], False)

    def testExecuteSortingStirring(self):
        #erste 5 Stationen in Reihe ausführen, dann mit robot 5 auf robot 4 und dann auf robot 6, danach wieder in Reihe
        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[0], False)

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[0], True)
        self.s.stationList[0].isExecuting = True

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go[0], True)
            self.s.stationList[0].isExecuting = False

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[1], True)
        self.s.stationList[1].isExecuting = True

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go[1], True)
            self.s.stationList[1].isExecuting = False

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[2], True)
        self.s.stationList[2].isExecuting = True

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go[2], True)
            self.s.stationList[2].isExecuting = False

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[3], True)
        self.s.stationList[3].isExecuting = True

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go[3], True)
            self.s.stationList[3].isExecuting = False

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[4], True)
        self.s.stationList[4].isExecuting = True

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go[4], True)
            self.s.stationList[4].isExecuting = False

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go[5], True)

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go2[0], True)

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go2[0], True)
            self.s.stationList[4].isExecuting = False

        self.s.executeSortingStirring()
        self.assertEqual(self.s.go2[1], True)

        for i in range(15):
            self.s.executeSortingStirring()
            self.assertEqual(self.s.go2[1], True)
            self.s.stationList[5].isExecuting = False

if __name__ == '__main__':
    unittest.main()
