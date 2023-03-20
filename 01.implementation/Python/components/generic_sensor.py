#!/usr/bin/env python

"""
generic_sensor.py: GenericSensor class

This is the root class for every sensor used in the simulation. 
It collects all the common fields and methods of any simulation sensor.  
"""

# NOTE: This class already has all the necessary fields and methods for any 
# generic sensor

class GenericSensor(object):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi, pin: int):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self.pin = pin
        # TODO: put pin feasibility check
        self.state = False
        self.getState()     # First reading of the actual state
    
    def getPin(self) -> int: 
        return self.pin

    def getState(self) -> bool:
        state = self.rpi.io['I_' + str(self.pin)].value
        if state == True:
            self.state = True
        else: 
            self.state = False
        return state
