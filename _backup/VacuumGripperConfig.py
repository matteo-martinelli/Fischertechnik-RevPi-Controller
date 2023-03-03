class VacuumGripperConfig:

    def __init__(self, counterVertical, counterRot, counterArm, gripperActive, endVertical=False, endRot=False, endArm=False):
        self.__counterVertical = counterVertical
        self.__counterRot = counterRot
        self.__counterArm = counterArm
        self.__gripperActive = gripperActive
        self.__endVertical = endVertical
        self.__endRot = endRot
        self.__endArm = endArm

    def __eq__(self, other):
        return (self.__endArm == other.endArm and
                self.__endRot == other.endRot and
                self.__endVertical == other.endVertical and
                self.counterArm == other.counterArm and
                self.gripperActive == other.gripperActive and
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
    def gripperActive(self):
        return self.__gripperActive

    @property
    def endVertical(self):
        return self.__endVertical

    @property
    def endRot(self):
        return self.__endRot

    @property
    def endArm(self):
        return self.__endArm

