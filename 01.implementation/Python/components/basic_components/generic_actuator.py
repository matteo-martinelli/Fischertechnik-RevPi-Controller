#!/usr/bin/env python

"""
generic_actuator.py: GenericActuator class

This is the root class for every actuator used in the simulation. 
It collects all the common fields and methods of any simulation actuator.  
"""

from typing import Union


class GenericActuator(object):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        #self.pin = pin
        # TODO: eventually assign directly here the pin from revpimodio
        self.pin_tuple = tuple() # add this thing to the subclass  
        # TODO: put pin feasibility check
        self.state = False  # TODO: eventually assign directly here the state from revpimodio
        # TODO change the first pin reading cause is wrong.
        #self.getState()     # First reading of the actual state
    
    def get_pin(self) -> Union[tuple,int]: 
        if len(self.pin_tuple) == 0: 
            return self.pin_tuple[0]
        elif len(self.pin_tuple) == 1: 
            return self.pin_tuple

    def get_state(self) -> Union[bool,str]:
        if len(self.pin_tuple) == 0: 
            self.state = self.rpi.io['O_' + str(self.pin_tuple[0])].value
        elif len(self.pin_tuple) == 1: 
            state_A = self.rpi.io['O_' + str(self.pin_tuple[0])].value
            state_B = self.rpi.io['O_' + str(self.pin_tuple[1])].value
            if (state_A == True and state_B == False):
                self.state = 'Pin 0 True'
            elif (state_A == False and state_B == True): 
                self.state = 'Pin 1 True'
            elif (state_A == False and state_B == False):
                self.state = False      # TODO: better False or 'off'??
            else: 
                self.state = 'Error'    # TODO: put a RaiseErrorException()
        return self.state
    
    def turn_on(self, *pin) -> None:
        pass

    def turn_off(self) -> None:
        self.state = False
        for i in range(len(self.pin_tuple)):
            self.rpi.io['O_' + str(self.pin_tuple[i])].value = self.state
    