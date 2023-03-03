import math
from abc import abstractmethod
from time import time


class Machine:
    def __init__(self, id1):
        self.__id = id1
        self.__isExecuting = False
        self.__lastExecutionTime = -math.inf


    @property
    def id(self) -> int:
        return self.__id

    @property
    @abstractmethod
    def isExecuting(self) -> bool:
        """Returns whether the machine is currently performing actions

        :return bool: the executing status
        """
        return self.__isExecuting
        #pass

    @isExecuting.setter
    def isExecuting(self, value: bool):
        self.__isExecuting = value
        if value:
            self.__lastExecutionTime = time()

    def timeSinceExecution(self):
        if self.__isExecuting:
            return 0
        else:
            return time() - self.__lastExecutionTime

    def execute(self, *args):
        pass
