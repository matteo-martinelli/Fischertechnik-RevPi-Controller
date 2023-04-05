#!/usr/bin/env python

"""
generic_sensor.py: GenericSensor class

This is the root class for every sensor used in the simulation. 
It collects all the common fields and methods of any simulation sensor.  
"""


class GenericRevPiSensor(object):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi, pin: int):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self.pin = pin  # TODO: eventually assign directly here the pin from revpimodio
        # TODO: put pin feasibility check
        self.state = False  # TODO: eventually assign directly here the state from revpimodio
        #self.get_state()     # First reading of the actual state
    
    def get_pin(self) -> int: 
        return self.pin

    def get_state(self) -> bool:
        self.state = self.rpi.io['I_' + str(self.pin)].value
        return self.state
