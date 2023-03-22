#!/usr/bin/env python

"""
vacuum_actuator.py: VacuumActuator class

For following pins: 
O_11: vacuum gripper on carrier activation;
O_12: vacuum gripper on carrier lowering;
O_13: vacuum activated oven doors opening;
O_14: turntable vacuum pusher activation.
"""

from components.basic_components.generic_actuator import GenericActuator


class VacuumActuator(GenericActuator):
    """Vacuum Actuator class for vacuum activated objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi)
        self.name = name
        self.pin_tuple = (pin,)


    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin_tuple[0])].value
        return self.state
    
    def turn_on(self) -> None: 
        self.state = True
        self.rpi.io['O_'+ str(self.pin_tuple[0])].value = self.state