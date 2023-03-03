class ThreeDRobotConfig:

    def __init__(self, counterVertical, counterRot, counterArm, counterGripper, endVertical=False, endRot=False, endArm=False, endGripper=False):
        self.__counterVertical = counterVertical
        self.__counterRot = counterRot
        self.__counterArm = counterArm
        self.__counterGripper = counterGripper
        self.__endVertical = endVertical
        self.__endRot = endRot
        self.__endArm = endArm
        self.__endGripper = endGripper

    def __eq__(self, other):
        return (self.__endArm == other.endArm and
                self.__endGripper == other.endGripper and
                self.__endRot == other.endRot and
                self.__endVertical == other.endVertical and
                self.counterArm == other.counterArm and
                self.counterGripper == other.counterGripper and
                self.counterRot == other.counterRot and
                self.counterVertical == other.counterVertical)

    @property
    def counterVertical(self):
        return self.__counterVertical

    @property
    def counterRot(self):
        return self.__counterRot

    @property
    def counterArm(self):
        return self.__counterArm

    @property
    def counterGripper(self):
        return self.__counterGripper

    @property
    def endVertical(self):
        return self.__endVertical

    @property
    def endRot(self):
        return self.__endRot

    @property
    def endArm(self):
        return self.__endArm

    @property
    def endGripper(self):
        return self.__endGripper
