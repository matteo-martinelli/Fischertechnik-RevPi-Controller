#!/usr/bin/env python

"""
vacuum_actuator.py: VacuumActuator class

For following pins: 
O_11: vacuum gripper on carrier activation;
O_12: vacuum gripper on carrier lowering;
O_13: vacuum activated oven doors opening;
O_14: turntable vacuum pusher activation.
"""

from components.basic_components.generic_revpi_actuator import \
    GenericRevPiActuator
from datetime import datetime
import time
import json

class RevPiVacuumActuator(GenericRevPiActuator):
    """Vacuum Actuator class for vacuum activated objects."""
    def __init__(self, rpi, name: str, pin: int, parent_topic: str, 
                 mqtt_publisher):
        super().__init__(rpi)
        self.name = name
        self.pin = pin
        # self.compressor = ... TODO: add compressor check
        # MQTT
        self.topic = parent_topic + '/actuators/' + name
        self.mqtt_publisher = mqtt_publisher


    # Getters
    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin)].value
        return self.state
    
    # Class Methods
    def turn_on(self) -> None: 
        if(self.state == False):
            self.state = True
            self.rpi.io['O_'+ str(self.pin)].value = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
             
    def turn_off(self) -> None:
        if(self.state == True):
            self.state = False
            self.rpi.io['O_'+ str(self.pin)].value = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

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
    