#!/usr/bin/env python

"""
light_barrier.py: LightBarrier class

For following pins: 
I_9: Oven; 
I_3: Conveyor.
"""

import revpimodio2
from mqtt.mqtt_publisher import MqttPublisher
from components.basic_components.generic_revpi_sensor import GenericRevPiSensor
from datetime import datetime
import time
import json


class RevPiLightBarrierSensor(GenericRevPiSensor):
    """Light Barrier class for light barrier objects."""
    def __init__(self, rpi: revpimodio2.RevPiModIO, name: str, pin: int, 
                 parent_topic: str, mqtt_publisher: MqttPublisher):
        super().__init__(rpi, pin)
        # MQTT
        self.topic = parent_topic + '/sensors/' + name
        self.mqtt_publisher = mqtt_publisher
        # Class fields
        self._name = name
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

    # Class methods
    def read_state(self) -> bool: 
        value = self.rpi.io['I_' + str(self.pin)].value
        self._state = value
        if(self._state != self._previous_state):
            self._previous_state = self._state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
        return self.state

    # MQTT 
    def to_dto(self) -> dict:
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

    def to_json(self) -> str:
        return json.dumps(self.to_dto())
