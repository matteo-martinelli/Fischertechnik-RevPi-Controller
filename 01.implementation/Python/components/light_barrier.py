#!/usr/bin/env python

"""
light_barrier.py: LightBarrier class

For following pins: 
I_9: Oven; 
I_3: Conveyor.
"""


class LightBarrier(object):
    """Light Barrier class for light barrier objects."""
    def __init__(self, rpi, name: str, pin: int):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self.name = name
        self.pin = pin
        self.state = False
        
        self.getState()     # First reading of the actual state

    def getName(self) -> str:
        return self.name
    
    def getState(self) -> bool:
        state = self.rpi.io['I_' + str(self.pin)].value
        if state == True:
            self.state = True
        else: 
            self.state = False
        
        # print('pin ' + str(self.pin) + ' ' + str(self.state))
        return state
