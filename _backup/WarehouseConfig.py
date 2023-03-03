class WarehouseConfig:

    def __init__(self,counterVertical,counterHorizontal,armEndIn,armEndOut,conveyorIn,conveyorOut,horizontalEnd=False,verticalEnd=False):
        self.__counterVertical = counterVertical
        self.__counterHorizontal = counterHorizontal
        self.__armEndIn = armEndIn
        self.__armEndOut = armEndOut
        if armEndOut and armEndIn:
            raise ValueError("both cant be true at the same time")
        self.__conveyorIn = conveyorIn
        self.__conveyorOut = conveyorOut
        if conveyorOut and conveyorIn:
            raise ValueError("both cant be true at the same time")
        self.__horizontalEnd = horizontalEnd
        self.__verticalEnd = verticalEnd

    def __eq__(self, other):
        return (self.__counterVertical == other.counterVertical and
                self.__counterHorizontal == other.counterHorizontal and
                self.__armEndIn == other.armEndIn and
                self.__armEndOut == other.armEndOut and
                self.__conveyorIn == other.conveyorIn and
                self.__conveyorOut == other.conveyorOut and
                self.__horizontalEnd == other.horizontalEnd and
                self.__verticalEnd == other.verticalEnd)

    @property
    def counterVertical(self):
        return self.__counterVertical

    @property
    def counterHorizontal(self):
        return self.__counterHorizontal

    @property
    def armEndIn(self):
        return self.__armEndIn

    @property
    def armEndOut(self):
        return self.__armEndOut

    @property
    def conveyorIn(self):
        return self.__conveyorIn

    @property
    def conveyorOut(self):
        return self.__conveyorOut

    @property
    def horizontalEnd(self):
        return self.__horizontalEnd

    @property
    def verticalEnd(self):
        return self.__verticalEnd
