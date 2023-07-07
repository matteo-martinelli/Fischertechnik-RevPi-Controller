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
        self.dept = dept
        self.station = station
        self.motor_state = False
        # MQTT
        self.mqtt_pub = mqtt_pub
        self.topic = self.dept + '/' + self.station 
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_pub)
        self.read_actuators()

    # Read all sensors and actuators
    def read_actuators(self) -> None: 
        self.set_motor_state()

    ## Setters ##
    # Actuator
    def set_motor_state(self) -> None: 
        value = self.motor.get_state()
        if (value != self.motor_state):
            self.motor_state = value

    ## Getters ##
    # Actuator
    def get_motor_state(self) -> bool:
        return self.motor_state
    
    # Class methods
    def activate_service(self):
        self.motor.turn_on()
        self.set_motor_state()
        print('compressor activated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())
        
    def deactivate_service(self):
        self.motor.turn_off()
        self.set_motor_state()
        print('compressor deactivated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())
        
    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'motor': self.motor.get_state(),
            
            'timestamp': timestamp,
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())