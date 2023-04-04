#!/usr/bin/env python

"""
light_barrier.py: LightBarrier class

For following pins: 
I_9: Oven; 
I_3: Conveyor.
"""

from components.basic_components.generic_revpi_sensor import GenericRevPiSensor
from datetime import datetime
import time
import json

class RevPiLightBarrierSensor(GenericRevPiSensor):
    """Light Barrier class for light barrier objects."""
    def __init__(self, rpi, name: str, pin: int, parent_topic: str, 
                 mqtt_publisher):
        super().__init__(rpi, pin)
        # MQTT
        self.topic = parent_topic + '/sensors/' + name
        self.mqtt_publisher = mqtt_publisher
        # Class fields
        self.name = name
        

    # Getters
    def get_name(self) -> str:
        return self.name
    
    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'pin': self.pin,
            'state': self.state,
            'type': self.__class__.__name__,
            'layer': 'sensor-actuator',
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
