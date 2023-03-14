#!/usr/bin/env python

"""
saw.py: Saw class

Add a description. 
"""


class TestActuator(object):
    """Saw class for saw objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
    
    def turn_on(self) -> None:     # O_4
        self.rpi.io['O_4'].value = True

    def turn_off(self) -> None:    # O_4
        self.rpi.io['O_4'].value = False

    def rf_sens(self) -> bool:       # I_5: vacuum carrier at turntable
        return self.rpi.io['I_5'].value

    def cycle_test(self):
        print(self.rf_sens())
        while (self.rf_sens() == True):
            self.turn_on()
            print('turned on')
        self.turn_off()
        print('turned off')