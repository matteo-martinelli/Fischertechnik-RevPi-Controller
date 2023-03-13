#!/usr/bin/env python

"""
saw.py: Saw class

Add a description. 
"""


class Saw(object):
    """Saw class for saw objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
    
    def conv_turn_on(self) -> None:     # O_3
        self.rpi.io['O_3'].value = True

    def conv_turn_off(self) -> None:    # O_3
        self.rpi.io['O_3'].value = False

    def rf_sens(self) -> bool:       # I_2
        return self.rpi.io['I_2'].value

    def cycle_test(self):
        if self.rf_sens() == True:
            self.conv_turn_on()
        else: 
            self.conv_turn_off()