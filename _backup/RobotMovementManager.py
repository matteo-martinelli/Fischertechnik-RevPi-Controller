from ThreeDRobotConfig import ThreeDRobotConfig


class RobotMovementManager:

    #TODO check all configs for valid movement range
    #TODO Wartezeiten nach move/Weiterschaltbedinung in Verbidnung mit execute in Robot.py

    @staticmethod
    def listForRobot1():
        list = []

        counterVertical = 1000
        counterRot = 500
        counterArm = 10
        counterGripper = 10
        endVertical = False
        endRot = False
        endArm = False
        endGripper = False

        list.append(ThreeDRobotConfig(counterVertical,counterRot,counterArm,counterGripper,endVertical,endRot,endArm,endGripper))

