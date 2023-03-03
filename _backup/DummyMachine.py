from Machine import Machine


class DummyMachine(Machine):

    def __init__(self, id1):
        super().__init__(id1)
        self.__isExecuting = False

    @property
    def isExecuting(self) -> bool:
        return self.__isExecuting

    @isExecuting.setter
    def isExecuting(self, value):
        self.__isExecuting = value

    def execute(self, *args):
        print("dummy machine executing " + str(self.id))
        return 1
