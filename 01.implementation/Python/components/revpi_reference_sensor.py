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

from components.basic_components.generic_revpi_sensor import GenericRevPiSensor
from datetime import datetime
import time
import json

class RevPiReferenceSensor(GenericRevPiSensor):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi, name: str, pin: int, parent_topic: str, 
                 mqtt_publisher):
        super().__init__(rpi, pin)
        # MQTT
        self.topic = parent_topic + '/sensors/' + name
        self.mqtt_publisher = mqtt_publisher
        # Class fileds
        self.name = name

    
    # Getters
    def get_name(self) -> str:
        return self.name
    
    def get_state(self) -> str:
        self.state = self.rpi.io['I_' + str(self.pin)].value
        if(self.state != self.previous_state):
            self.previous_state = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                    self.to_json())
        return self.state
    
    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

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
