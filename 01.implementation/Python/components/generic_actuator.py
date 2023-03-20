#!/usr/bin/env python

"""
generic_actuator.py: GenericActuator class

This is the root class for every actuator used in the simulation. 
It collects all the common fields and methods of any simulation actuator.  
"""


class GenericActuator(object):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        #self.pin = pin
        self.pin_tuple = tuple() # add this thing to the subclass  
        # TODO: put pin feasibility check
        self.state = False
        # TODO change the first pin reading cause is wrong.
        #self.getState()     # First reading of the actual state
    
    def getPin(self, pos) -> tuple: 
        return self.pin_tuple

    def getState(self) -> bool:
        #state = self.rpi.io['I_' + str(self.pin)].value
        #self.state = state

        #if state == True:
        #    self.state = True
        #else: 
        #    self.state = False
        
        #return self.state
        pass

    def turn_on(self) -> None:
        pass

    def turn_off(self) -> None:
        self.state = False
        for i in range(len(self.pin_tuple)):
            self.rpi.io['O_' + str(self.pin_tuple[i])].value = self.state
    