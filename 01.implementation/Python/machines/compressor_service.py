#!/usr/bin/env python

"""
compressor_service.py: CompressorService class

For following pins: 
O_10: compressor.
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from datetime import datetime
import time
import json


class CompressorService(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, dept: str, station: str, motor_act_pin: int, 
                 mqtt_pub):
        # Class descriptive fields
        self._dept = dept
        self._station = station
        self._motor_state = False
        # MQTT
        self.mqtt_pub = mqtt_pub
        self.topic = self._dept + '/' + self._station 
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_pub)
        self.read_all_actuators()


    # Getters
    @property
    def motor_state(self) -> bool:
        return self._motor_state
    
    # Setters
    @motor_state.setter
    def motor_state(self, value: bool) -> None: 
        #value = self.motor.get_state()
        if (value != self._motor_state):
            self._motor_state = value
    
    # Class methods
    def activate_service(self):
        self.motor.turn_on()
        self._motor_state = True
        print('compressor activated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())
        
    def deactivate_service(self):
        self.motor.turn_off()
        self._motor_state = False
        print('compressor deactivated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())

    # Reading underlying sensors/actuators
    def read_motor_state(self) -> None: 
        value = self.motor.state
        if(value != self._motor_state):
            self._motor_state = value
            self.mqtt_pub.publish_telemetry_data(self.topic, \
                                                       self.to_json())

    def read_all_actuators(self) -> None: 
        self.read_motor_state
    
    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'motor': self.motor.state,
            
            'timestamp': timestamp,
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())