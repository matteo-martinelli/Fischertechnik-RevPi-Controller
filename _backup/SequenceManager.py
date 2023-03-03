from typing import List

from Machine import Machine
from CyclicWaiter import CyclicWaiter
from copy import deepcopy


class SequenceManager:

    def __init__(self, id1, *managedStations: Machine):
        self.__isleId = id1
        self.__stationList = []
        self.wait = CyclicWaiter(15)
        self.__first = True
        self.__go = []
        self.__go2 = []
        self.index = 0
        self.__t2 = False
        for m in managedStations:
            self.__stationList.append(m)
        #TODO list creation in methoden mit try auslagern
        self.__subStationList1 = []
        self.__subStationList2 = []
        self.buildGraph()

    # maschine vllt mit "ein/Ausgängen", Materialquelle an stellen wo turtlebot anliefert/Senken wo abgeholt wird
    # TODO implement successor/predecessor function to determine flow through stations (with predeccessor/successor as machine attributes
    # roboter, vacuumgreifer kann mehere vorgänger/nachfolger haben
    # execute von moving machine mit übergabeparametern
    def buildGraph(self):
        self.__subStationList1 = self.__stationList[0:5]
        self.__subStationList2.append(self.__stationList[4])
        self.__subStationList2.append(self.__stationList[3])
        self.__subStationList2.append(self.__stationList[5])
        self.__subStationList2.append(self.__stationList[6])
        self.__subStationList2.append(self.__stationList[7])

    def inOrderExecutor(self, orderedList: List[Machine], goList: List[bool]):
        if self.__first:
            self.__first = False
            for i in orderedList:
                goList.append(False)
            goList.append(False)
        else:
            if True in goList:
                self.index = goList.index(True)
                if self.index < len(goList) - 1:
                    goList[self.index] = False
                    goList[self.index + 1] = True
                else:
                    goList[self.index] = False
            else:
                goList[0] = True


    def executeSortingStirring(self):
        #TODO Logik real implementieren, hier nur beispielhaft
        #0: 3D Roboter Anfang
        #1: Conveyor Anfang
        #2: Sorting Line
        #3: Vacuum Gripper
        #4: High Bay
        #5: Indexed Line
        #6: 3D Roboter Ende
        #7: Conveyor Ende
        #self.__stationList[0].execute(0,1)
        if True in self.__go and not self.__t2:
            index = self.__go.index(True)
            #print(index)
            start = fin = -1
            if index == 0:
                start = 0
                fin = 1
            if index == 3:
                start = 3
                fin = 0
                try:
                    self.__subStationList1[1].stop()
                except Exception as e:
                    pass
            if index == 4:
                start = 0
                fin = 1
            print(self.__subStationList1[index].__class__.__name__)
            try:
                self.__subStationList1[index].execute(start,fin)
            except TypeError as e:
                self.__subStationList1[index].execute()

            try:
                self.__subStationList1[index-1].pc = 0
            except Exception as e:
                pass

            if not self.__subStationList1[index].isExecuting and self.wait.wait():
                self.wait.reset()
                self.inOrderExecutor(self.__subStationList1, self.__go)
                print(self.__go)
        elif not self.__t2:
            self.inOrderExecutor(self.__subStationList1, self.__go)

        if self.__go[5] and not self.__t2:
            self.__t2 = True
            print("print now list 2")
            self.__first = True
            self.__subStationList1[2].once = True
            self.__go2 = []
            
            self.index = 0
        if self.__t2:
            if True in self.__go2:
                index = self.__go2.index(True)
                #print(index)
                start = fin = -1
                if index == 0:
                    start = 2
                    fin = 0
                if index == 1:
                    start = 0
                    fin = 4
                if index == 3:
                    start = 0
                    fin = 1
                print(self.__subStationList2[index].__class__.__name__)
                try:
                    self.__subStationList2[index].execute(start,fin)
                except TypeError as e:
                    self.__subStationList2[index].execute()

                try:
                    self.__subStationList2[index-1].pc = 0
                except Exception as e:
                    pass

                #print(self.__stationList[index].isExecuting)
                if not self.__subStationList2[index].isExecuting and self.wait.wait():
                    self.wait.reset()
                    self.inOrderExecutor(self.__subStationList2, self.__go2)
                    print("go2")
                    print(self.__go2)

                if self.__go2[5] and self.__t2:
                    try:
                        self.__subStationList2[4].stop()
                    except Exception as e:
                        pass
                    self.__t2 = False
                    print("now list 1 again")
                    self.__first = True
                    self.__go = []
            else:
                self.inOrderExecutor(self.__subStationList2, self.__go2)
                print("go2")
                print(self.__go2)


    @property
    def go(self):
        return deepcopy(self.__go)

    @property
    def go2(self):
        return deepcopy(self.__go2)

    @property
    def stationList(self):
        return deepcopy(self.__stationList)



