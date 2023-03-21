#!/usr/bin/env python

"""
reference_switch.py: ReferenceSwitch class

For following pins:
I_1: Turntable under vacuum carrier; 
I_2: Turntable aligned to position conveyor;
I_4: Turn-table under saw; 
I_5: Vacuum carrier aligned to turn-table; 
I_6: Oven carrier inside the oven; 
I_7: Oven carrier outside the oven; 
I_8: Vacuum carrier aligned to oven; 
"""

from basic_components.generic_sensor import GenericSensor


class ReferenceSwitch(GenericSensor):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi, pin)
        self.name = name

    
    def getName(self) -> str:
        return self.name
