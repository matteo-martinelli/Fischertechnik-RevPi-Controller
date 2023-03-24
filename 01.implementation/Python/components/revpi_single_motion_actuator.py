#!/usr/bin/env python

"""
single_motion_actuator.py: SingleMotionActuator class

For following pins: 
O_3: conveyor belt;
O_4: saw; 
O_9: processing light;
O_10: compressor.
"""

from components.basic_components.generic_revpi_actuator import GenericActuator


class RevPiSingleMotionActuator(GenericActuator):
    """Single Motion Actuator class for single motion actuated objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi)
        self.name = name
        self.pin = pin
        self.get_state()


    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin)].value
        return self.state
    
    def turn_on(self) -> None:
        self.state = True
        self.rpi.io['O_'+ str(self.pin)].value = self.state
    
    def turn_off(self) -> None:
        self.state = False
        self.rpi.io['O_'+ str(self.pin)].value = self.state
