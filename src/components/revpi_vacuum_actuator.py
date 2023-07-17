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
        self._name = name
        self._pin = pin
        # self.compressor = ... TODO: add compressor check
        # MQTT
        self.topic = parent_topic + '/actuators/' + name
        self.mqtt_publisher = mqtt_publisher
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
        value = self.rpi.io['O_'+ str(self._pin)].value
        self._state = value
        if(self.state != self._previous_state):
            self._previous_state = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
        return self.state

    def turn_on(self) -> None: 
        if(self.state == False):
            self.state = True
            self.rpi.io['O_'+ str(self._pin)].value = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
             
    def turn_off(self) -> None:
        if(self.state == True):
            self.state = False
            self.rpi.io['O_'+ str(self._pin)].value = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'type': self.__class__.__name__,
            'layer': 'sensor-actuator',
            'pin': self._pin,
            'state': self.state,
            
            'timestamp': timestamp,
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
    