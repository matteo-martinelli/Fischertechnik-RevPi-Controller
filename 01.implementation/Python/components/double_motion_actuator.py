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

from components.generic_actuator import GenericActuator

class DoubleMotionActuator(GenericActuator):
    """Double Activation Motor class for double motor actuated objects."""
    def __init__(self, rpi, pin_A: int, pin_B: int):
        super().__init__(rpi)
        #self.name = name
        self.pin_tuple = (pin_A, pin_B)
        # Instantiate RevPiModIO controlling library
        #self.rpi = rpi
        #self.name = name
        #self.pin_dir_A = pin_A
        #self.pin_dir_B = pin_B
        self.state = False
        # TODO change the first pin reading cause is wrong.
        self.getState()     # First reading of the actual state

    #def getName(self) -> str:
    #    return self.names

    def getState(self) -> None:
        state_A = self.rpi.io['O_' + str(self.pin_tuple[0])].value
        state_B = self.rpi.io['O_' + str(self.pin_tuple[1])].value
        if (state_A == True and state_B == False):
            self.state = 'Towards A'
        elif (state_A == False and state_B == True): 
            self.state = 'Towards B'
        elif (state_A == False and state_B == False):
            self.state = False
        else: 
            self.state = 'Error'    # TODO: put a RaiseErrorException()
        return self.state
    
    def move_towards_A(self) -> None:
        """
        Following actions: 
        O_1: turntable clockwise
        O_5: oven carrier inside
        O_7: vacuum carrier towards oven
        
        self.state = 'Towards A'
        self.rpi.io['O_' + str(self.pin_dir_A)].value = True
        self.rpi.io['O_' + str(self.pin_dir_B)].value = False
        """
        self.turn_on(self.pin_tuple[0])

    def move_towards_B(self) -> None:
        """
        Following actions: 
        O_2: turntable counter-clockwise
        O_6: oven carrier outside
        O_8: vacuum carrier towards turntable
        self.state = 'Towards B'
        self.rpi.io['O_' + str(self.pin_dir_A)].value = False
        self.rpi.io['O_' + str(self.pin_dir_B)].value = True
        """
        self.turn_on(self.pin_tuple[1])

    def turn_on(self, activation_pin: int):
        for i in range(len(self.pin_tuple)):
            if self.pin_tuple[i] == activation_pin: 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = True
                self.state = True
            else: 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = False
    """
    def turn_off(self) -> None:
        self.state = 'Off'
        self.rpi.io['O_' + str(self.pin_dir_A)].value = False
        self.rpi.io['O_' + str(self.pin_dir_B)].value = False
    """
