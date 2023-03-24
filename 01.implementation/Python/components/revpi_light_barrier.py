#!/usr/bin/env python

"""
light_barrier.py: LightBarrier class

For following pins: 
I_9: Oven; 
I_3: Conveyor.
"""

from components.basic_components.generic_revpi_sensor import GenericSensor


class RevPiLightBarrier(GenericSensor):
    """Light Barrier class for light barrier objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi, pin)
        self.name = name
        

    def get_name(self) -> str:
        return self.name
