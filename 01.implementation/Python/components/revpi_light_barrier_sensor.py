#!/usr/bin/env python

"""
light_barrier.py: LightBarrier class

For following pins: 
I_9: Oven; 
I_3: Conveyor.
"""

from components.basic_components.generic_revpi_sensor import GenericRevPiSensor
import json
import datetime

class RevPiLightBarrierSensor(GenericRevPiSensor):
    """Light Barrier class for light barrier objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi, pin)
        self.name = name
        

    def get_name(self) -> str:
        return self.name
    
    # MQTT 
    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'pin': self.pin,
            'state': self.state,
            'timestamp': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
