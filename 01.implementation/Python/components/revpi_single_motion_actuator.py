#!/usr/bin/env python

"""
single_motion_actuator.py: SingleMotionActuator class

For following pins: 
O_3: conveyor belt;
O_4: saw; 
O_9: processing light;
O_10: compressor.
"""
import paho.mqtt.client as mqtt
from conf.mqtt_conf_parameters import MqttConfiguratorParameter
from components.basic_components.generic_revpi_actuator import GenericRevPiActuator
from datetime import datetime
import json


class RevPiSingleMotionActuator(GenericRevPiActuator):
    """Single Motion Actuator class for single motion actuated objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi)
        self.name = name
        self.pin = pin
        self.get_state()


    # Getters
    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin)].value
        return self.state
    # Class Methods
    def turn_on(self) -> None:
        self.state = True
        self.rpi.io['O_'+ str(self.pin)].value = self.state
    
    def turn_off(self) -> None:
        self.state = False
        self.rpi.io['O_'+ str(self.pin)].value = self.state

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

