#!/usr/bin/env python

"""
single_motion_actuator.py: SingleMotionActuator class

For following pins: 
O_3: conveyor belt;
O_4: saw; 
O_9: processing light;
O_10: compressor.
"""

from components.basic_components.generic_revpi_actuator import \
    GenericRevPiActuator
from datetime import datetime
import time
import json


class RevPiSingleMotionActuator(GenericRevPiActuator):
    """Single Motion Actuator class for single motion actuated objects."""
    def __init__(self, rpi, name: str, pin: int, parent_topic: str, 
                 mqtt_publisher):
        super().__init__(rpi)
        # MQTT
        self.topic = parent_topic + '/actuators/' + name
        self.mqtt_publisher = mqtt_publisher
        # Class fields
        self.name = name
        self.pin = pin
        # Fields init
        self.read_state()

    
    # Getters
    @property
    def name(self) -> str: 
        return self._name
    
    @property
    def state(self) -> bool: 
        return self._state
    
    # Setters
    @name.setter
    def name(self, value: str) -> None: 
        self._name = value

    @state.setter
    def state(self, value: bool) -> None: 
        self._state = value
    
    # Class Methods
    def read_state(self) -> bool: 
        value = self.rpi.io['O_'+ str(self.pin)].value
        self.state = value
        if(self.state != self._previous_state):
            self._previous_state = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
        return self.state

    def turn_on(self) -> None:
        if (self.state == False):
            self.state = True
            self.rpi.io['O_'+ str(self.pin)].value = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    def turn_off(self) -> None:
        if (self.state == True):
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
            'type': self.__class__.__name__,
            'layer': 'sensor-actuator',
            'pin': self.pin,
            'state': self.state,

            'timestamp': timestamp, 
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
