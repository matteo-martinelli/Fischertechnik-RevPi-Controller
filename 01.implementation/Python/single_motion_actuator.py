#!/usr/bin/env python

"""
single_motion_actuator.py: SingleMotionActuator class

For following pins: 
O_3: conveyor belt;
O_4: saw; 
O_9: processing light;
O_10: compressor.
"""


class SingleMotionActuator(object):
    """Single Motion Actuator class for single motion actuated objects."""
    def __init__(self, rpi, name: str, pin: int):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self.name = name
        self.pin = pin
        # TODO: put pin validity check - it should be between 1 and 14
        self.state = False
        self.getState()     # First reading of the actual state

    def getName(self) -> str:
        return self.name
    
    def getState(self) -> bool:
        state = self.rpi.io['O_' + str(self.pin)].value
        return state
    
    def turn_on(self) -> None:
        self.state = True
        self.rpi.io['O_' + str(self.pin)].value = self.state

    def turn_off(self) -> None:
        self.state = False
        self.rpi.io['O_' + str(self.pin)].value = self.state
