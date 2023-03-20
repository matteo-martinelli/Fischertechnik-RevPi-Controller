#!/usr/bin/env python

"""
double_motion_actuator.py: DoubleMotionActuator class

For following pins: 
O_1: turntable clockwise
O_2: turntable counter-clockwise
O_5: oven carrier inside
O_6: oven carrier outside
O_7: vacuum carrier towards oven
O_8: vacuum carrier towards turntable
"""


class DoubleMotionActuator(object):
    """Double Activation Motor class for double motor actuated objects."""
    def __init__(self, rpi, name: str, pin_A: int, pin_B: int):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self.name = name
        self.pin_dir_A = pin_A
        self.pin_dir_B = pin_B
        self.state = 'Off'

        self.getState()     # First reading of the actual state

    def getName(self) -> str:
        return self.name
    
    def getState(self) -> bool:
        state_A = self.rpi.io['O_' + str(self.pin_dir_A)].value
        state_B = self.rpi.io['O_' + str(self.pin_dir_B)].value
        if (state_A == True and state_B == False):
            self.state = 'Towards A'
        elif (state_A == False and state_B == True): 
            self.state = 'Towards B'
        elif (state_A == False and state_B == False):
            self.state = 'Off'
        else: 
            self.state = 'Error'    # TODO: put a RaiseErrorException()
        return self.state
    
    def move_towards_A(self) -> None:
        """
        Following actions: 
        O_1: turntable clockwise
        O_5: oven carrier inside
        O_7: vacuum carrier towards oven
        """
        self.state = 'Towards A'
        self.rpi.io['O_' + str(self.pin_dir_A)].value = True
        self.rpi.io['O_' + str(self.pin_dir_B)].value = False

    def move_towards_B(self) -> None:
        """
        Following actions: 
        O_2: turntable counter-clockwise
        O_6: oven carrier outside
        O_8: vacuum carrier towards turntable
        """
        self.state = 'Towards B'
        self.rpi.io['O_' + str(self.pin_dir_A)].value = False
        self.rpi.io['O_' + str(self.pin_dir_B)].value = True

    def turn_off(self) -> None:
        self.state = 'Off'
        self.rpi.io['O_' + str(self.pin_dir_A)].value = False
        self.rpi.io['O_' + str(self.pin_dir_B)].value = False
