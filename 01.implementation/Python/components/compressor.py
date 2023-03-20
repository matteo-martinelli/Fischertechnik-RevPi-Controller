#!/usr/bin/env python

"""
compressor.py: Compressor class

For following pins: 
O_10: compressor.
"""

# TODO: import single motion actuator?

class Compressor(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, name: str, pin: int):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self.name = name
        self.pin = pin
        self.state = 'Off'

        self.getState()     # First reading of the actual state

    def getName(self) -> str:
        return self.name
    
    def getState(self) -> bool:
        state = self.rpi.io['O_' + str(self.pin)].value
        if state == True:
            self.state = 'On'
        else: 
            self.state = 'Off'
        return state
    
    def turn_on(self) -> None:
        self.state = 'On'
        self.rpi.io['O_' + str(self.pin)].value = True

    def turn_off(self) -> None:
        self.state = 'Off'
        self.rpi.io['O_' + str(self.pin)].value = False
