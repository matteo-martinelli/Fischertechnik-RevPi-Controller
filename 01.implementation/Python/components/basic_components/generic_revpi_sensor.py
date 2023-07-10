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
        # TODO: eventually assign directly here the pin from revpimodio
        # TODO: put pin feasibility check
        self._pin = pin
        # TODO: eventually assign directly here the state from revpimodio
        self._state = False
        self._previous_state = False
        
    # Getters
    @property
    def pin(self) -> int: 
        return self._pin

    @property
    def state(self) -> bool: 
        return self._state
    
    @property
    def previous_state(self) -> bool: 
        return self._previous_state

    # Setters
    @pin.setter
    def pin(self, value: int) -> None: 
        self._pin = value

    @state.setter
    def state(self, value: bool) -> None: 
        self._state = value

    @previous_state.setter
    def previous_state(self, value: bool) -> None: 
        self._previous_state = value

    # Class methods
    def read_state(self) -> None:
        value = self.rpi.io['I_' + str(self.pin)].value
        self._state = value
