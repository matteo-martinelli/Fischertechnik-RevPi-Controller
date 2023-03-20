#!/usr/bin/env python

"""
compressor.py: Compressor class

For following pins: 
O_10: compressor.
"""

from components.single_motion_actuator import SingleMotionActuator


class Compressor(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, name: str, pin: int):
        self.motor = \
            SingleMotionActuator(rpi, 'compressor motor', 10)

    
    def getState(self) -> bool:
        return self.motor.getState()
            
    def turn_on(self) -> None:
        self.motor.turn_on()
        
    def turn_off(self) -> None:
        self.motor.turn_off()
