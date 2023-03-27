#!/usr/bin/env python

"""
compressor.py: Compressor class

For following pins: 
O_10: compressor.
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
import json


class Compressor(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, pin: int):
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'compressor motor', pin)
        #self.name = pin 


    def activate(self):
        self.motor.turn_on()
        #print(self.motor.to_json())
