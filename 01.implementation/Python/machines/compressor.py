#!/usr/bin/env python

"""
compressor.py: Compressor class

For following pins: 
O_10: compressor.
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator


class Compressor(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, pin: int):
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'compressor motor', pin)


"""
    def get_state(self) -> bool:
        return self.motor.get_state()
            
    def turn_on(self) -> None:
        self.motor.turn_on()
        
    def turn_off(self) -> None:
        self.motor.turn_off()
"""