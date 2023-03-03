#!/usr/bin/env python
# never make any changes above this line
#----------------------------------------#

#use this import for use in IDE as site package
from pixtendlib.pixtendv2l import PiXtendV2L
#use this import for running on raspi
#from pixtendv2l import PiXtendV2L

from time import sleep
from time import time

from Robot import Robot
from RobotMovementManager import RobotMovementManager

# VAR

#robot1 = Robot(1, RobotMovementManager.listForRobot1())

inputs = []
outputs = []
#ENDVAR


# Using the PiXtendV2L object, all I/O Ports are read - if not otherwise specified in the Constructor - every 30ms.
# the p object delivers and takes the values ON and OFF, so for use in Python they should be converted to True and False
def read():
    #read all inputs
    inputs.clear()
    inputs.append(p.digital_in0)
    inputs.append(p.digital_in1)
    inputs.append(p.digital_in2)
    inputs.append(p.digital_in3)
    inputs.append(p.digital_in4)
    inputs.append(p.digital_in5)
    inputs.append(p.digital_in6)
    inputs.append(p.digital_in7)
    inputs.append(p.digital_in8)
    inputs.append(p.digital_in9)
    inputs.append(p.digital_in10)
    inputs.append(p.digital_in11)
    inputs.append(p.digital_in12)
    inputs.append(p.digital_in13)
    inputs.append(p.digital_in14)
    inputs.append(p.digital_in15)
    print(inputs)
    #set all attributes to work with in class
    i = 0
    robot1.robotSensGripperOpen = inputs[i]
    i += 1
    robot1.robotSensGripperImpulse = inputs[i]
    i += 1
    robot1.robotSensArmEndIn = inputs[i]
    i += 1
    robot1.robotSensArmImpulse = inputs[i]
    i += 1
    robot1.robotSensVerticalEndUp = inputs[i]
    i += 1
    robot1.robotSensRotEnd = inputs[i]
    i += 1
    robot1.robotSensVerticalImpulse1 = inputs[i]
    i += 1
    robot1.robotSensVerticalImpulse2 = inputs[i]
    i += 1
    robot1.robotSensRotImpulse1 = inputs[i]
    i += 1
    robot1.robotSensRotImpulse2 = inputs[i]
    i += 1


def write():
    p.digital_out0 = robot1.robotActGripperOpen
    p.digital_out1 = robot1.robotActGripperClose
    p.digital_out2 = robot1.robotActArmOut
    p.digital_out3 = robot1.robotActArmIn
    p.digital_out4 = robot1.robotActVerticalDown
    p.digital_out5 = robot1.robotActVerticalUp
    p.digital_out6 = robot1.robotActRotRight
    p.digital_out7 = robot1.robotActRotLeft
    p.digital_out8 = False
    p.digital_out9 = False
    p.digital_out10 = False
    p.digital_out11 = False
    outputs.clear()
    outputs.append(robot1.robotActGripperOpen)
    outputs.append(robot1.robotActGripperClose)
    outputs.append(robot1.robotActArmOut)
    outputs.append(robot1.robotActArmIn)
    outputs.append(robot1.robotActVerticalDown)
    outputs.append(robot1.robotActVerticalUp)
    outputs.append(robot1.robotActRotRight)
    outputs.append(robot1.robotActRotLeft)
    outputs.append(False)
    outputs.append(False)
    outputs.append(False)
    outputs.append(False)
    print(outputs)


def gotoSaveState():
    global p
    p.digital_out0 = False
    p.digital_out1 = False
    p.digital_out2 = False
    p.digital_out3 = False
    p.digital_out4 = False
    p.digital_out5 = False
    p.digital_out6 = False
    p.digital_out7 = False
    p.digital_out8 = False
    p.digital_out9 = False
    p.digital_out10 = False
    p.digital_out11 = False
    sleep(1)
    p.close()
    #del p


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global p
    p = PiXtendV2L()
    robot1 = Robot(1, [])
    try:
        while True:
            print(time())
            read()
            robot1.executeDummy()
            write()
            sleep(0.03)
    except KeyboardInterrupt:
        gotoSaveState()
    except Exception:
        gotoSaveState()
        raise Exception
