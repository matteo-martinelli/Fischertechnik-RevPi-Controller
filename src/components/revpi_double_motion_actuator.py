#!/usr/bin/env python

"""
double_motion_actuator.py: DoubleMotionActuator class

For following pins: 
O_1: turntable clockwise
O_2: turntable counter-clockwise
O_5: oven carrier inside
O_6: oven carrier outside
O_7: vacuum carrier towards oven
O_8: vacuum carrier towards turntable
"""

import revpimodio2
from mqtt.mqtt_publisher import MqttPublisher
from components.basic_components.generic_revpi_actuator import GenericRevPiActuator
from datetime import datetime
import time
import json


class RevPiDoubleMotionActuator(GenericRevPiActuator):
    """Double Activation Motor class for double motor actuated objects."""
    def __init__(self, rpi: revpimodio2.RevPiModIO, name: str, pin_A: 
                 int, pin_B: int, parent_topic: str, mqtt_publisher: MqttPublisher):
        super().__init__(rpi)
        # MQTT
        self.topic = parent_topic + '/actuators/' + name
        self.mqtt_publisher = mqtt_publisher
        # Class fields
        self._state = (False, False)
        self._name = name
        self._pin_tuple = (pin_A, pin_B)
        # Fields init
        self.read_state()
    

    # Getters
    @property
    def state(self) -> tuple: 
        return self._state
    
    @property
    def name(self) -> str:
        return self._name
    
    # Setters
    @state.setter
    def state(self, value_pin_A: bool, value_pin_B: bool) -> None:
        self._state = (value_pin_A, value_pin_B) 

    @name.setter
    def name(self, value: str) -> None: 
        self._name = value

    # Class Methods
    def read_state(self) -> tuple:
        state_A = self.rpi.io['O_' + str(self._pin_tuple[0])].value
        state_B = self.rpi.io['O_' + str(self._pin_tuple[1])].value
        self._state = (state_A, state_B)
        if(self.state != self._previous_state):
            self.previous_state = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
        return self._state

    def turn_on(self, activation_pin: int) -> None:
        for i in range(len(self._pin_tuple)):
            if (self._pin_tuple[i] == activation_pin and 
                self.rpi.io['O_' + str(self._pin_tuple[i])].value == False): 
                self.rpi.io['O_' + str(self._pin_tuple[i])].value = True
                self.read_state()
            else: 
                self.rpi.io['O_' + str(self._pin_tuple[i])].value = False
                self.read_state()
        
    def turn_off(self) -> None:
        if (self._state[0] != False or self._state[1] != False):
            self._state = (False, False)
            for i in range(len(self._pin_tuple)):
                self.rpi.io['O_' + str(self._pin_tuple[i])].value = False
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # MQTT 
    def to_dto(self) -> dict:
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'type': self.__class__.__name__,
            'layer': 'sensor-actuator',
            'pins': self._pin_tuple,
            'state': self.state,
            
            'timestamp': timestamp,
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dto())