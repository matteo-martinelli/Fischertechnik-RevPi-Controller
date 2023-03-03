class ReachedDirection:
    def __init__(self, bool, dirArm, dirGripper):
        self.__reached = bool
        self.__directionArm = dirArm
        self.__directionGripper = dirGripper

    @property
    def reached(self):
        return self.__reached

    @property
    def directionArm(self):
        return self.__directionArm

    @property
    def directionGripper(self):
        return self.__directionGripper
