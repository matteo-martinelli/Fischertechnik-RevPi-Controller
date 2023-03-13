#!/usr/bin/env python

"""
vacuum_actuator.py: VacuumActuator class

For following pins: 
O_11: vacuum gripper on carrier activation;
O_12: vacuum gripper on carrier lowering;
O_13: vacuum activated oven doors opening;
O_14: turntable vacuum pusher activation.
"""


class VacuumActuator(object):
    """Compressor class for compressor objects."""
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
