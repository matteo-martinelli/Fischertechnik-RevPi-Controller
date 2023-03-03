from abc import abstractmethod
from Machine import Machine
from copy import deepcopy


# this class should be used for all machines, that have no strict movement path, but can follow various paths
# examples: Warehouse, 3D Robot
class MovingMachine(Machine):

    @property
    @abstractmethod
    def isExecuting(self) -> bool:
        pass

    def __init__(self, id1: int, placeList: list) -> None:
        """Init for a moving machine, additionally needs a list of places where pick/place operations could be performed

        :param int id1: the machine id
        :param list placeList: the list of places
        """
        super().__init__(id1)
        self.__placeList = placeList
        self.__configGoal = None
        self.__configReached = False
        self.__setupFinished = self.setupFinishedHelper = False
        self.__pc = 0
        self.__moveList = []
        self.start = self.fin = 0

    @property
    def placeList(self) -> list:
        """Returns the list of all specified places the machine uses

        :returns: a deepcopy of the list
        :rtype: list
        """
        return deepcopy(self.__placeList)

    @abstractmethod
    def generateTransferMoveList(self, numPickup: int, numPlace: int) -> list:
        """Uses the known places specified as Pickup location or Place location to create a move list

        :param int numPickup: location at this index in the place list is the place object is picked up at
        :param int numPlace: location at this index in the place list is the place object is dropped up at

        :returns: configs specific to the machine to travel between the places
        :rtype: list
        """
        pass

    def setup(self) -> bool:
        """Performs the setup of the machine to ensure all counters are correctly set

        :return bool: True if the setup is finished
        """
        pass

    def gotoConfig(self, config) -> bool:
        """Takes all necessary actions to ensure the machine reaches the specified config

        :param config: a config object fitting the machine type
        :returns bool: True if the config is reached
        """
        pass

    def execute(self, start: int, fin: int) -> None:
        """execute performs the action indicated by the input numbers to move the robot between the two specified places

        :param int start: see method generate transferMoveList
        :param int fin: see method generate transferMoveList
        """
        #pc rücksetzen für neue move list wenn sich eingabe von start oder zielposition ändert
        if self.start != start or self.fin != fin:
            self.start = start
            self.fin = fin
            self.__pc = 0
        #TODO pc auch zurücksetzen wenn erneute Ausführung
        if not self.__setupFinished:
            self.__setupFinished = self.setup()
            self.setupFinishedHelper = self.__setupFinished
            self.__configReached = True
        else:
            self.__moveList = []
            self.__moveList.extend(self.generateTransferMoveList(start,fin))
            #print(self.__moveList)
            #fahre zur position
            if self.__configReached:
                print("config reached")
                self.__configReached = False
                #weitere moves vorhanden
                if self.__pc < len(self.__moveList):
                    print("next move")
                    self.__configGoal = self.__moveList[self.__pc]
                    self.__pc += 1
                    print(self.__pc)
                else:
                    #TODO reactivate if necessary self.__pc = 0
                    pass
            self.__configReached = self.gotoConfig(self.__configGoal)

    @property
    def pc(self) -> int:
        """Returns the pc indicating the current executing position in the move list

        :returns: the pc value
        :rtype: int
        """
        return self.__pc


    @pc.setter
    def pc(self, value):
        self.__pc = value
