#!/usr/bin/env python

"""
light_barrier.py: LightBarrier class

For following pins: 
I_9: Oven; 
I_3: Conveyor.
"""

from components.generic_sensor import GenericSensor


class LightBarrier(GenericSensor):
    """Light Barrier class for light barrier objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi, pin)
        self.name = name
        

    def getName(self) -> str:
        return self.name
