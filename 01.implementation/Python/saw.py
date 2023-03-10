#!/usr/bin/env python

"""
saw.py: Saw class

Add a description. 
"""


import revpimodio2

class Saw(object):
    """Saw class for saw objects."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
    
    def turn_on(self):
        self.rpi.io['O_4'].value = True

    def turn_off(self):
        self.rpi.io['O_4'].value = False