#!/usr/bin/env python

"""
reference_switch.py: ReferenceSwitch class

For following pins:
I_1: Turntable under vacuum carrier; 
I_2: Turntable aligned to position conveyor;
I_4: Turn-table under saw; 
I_5: Vacuum carrier aligned to turn-table; 
I_6: Oven carrier inside the oven; 
I_7: Oven carrier outside the oven; 
I_8: Vacuum carrier aligned to oven; 
"""


class ReferenceSwitch(object):
    """Reference Switch class for reference switch objects."""
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
