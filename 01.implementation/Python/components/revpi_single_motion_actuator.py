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
        self.get_state()


    # Getters
    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin)].value
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        return self.state
    
    # Class Methods
    def turn_on(self) -> None:
        self.state = True
        self.rpi.io['O_'+ str(self.pin)].value = self.state
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    def turn_off(self) -> None:
        self.state = False
        self.rpi.io['O_'+ str(self.pin)].value = self.state
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

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
