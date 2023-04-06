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
        # MQTT
        self.mqtt_pub = mqtt_pub
        self.topic = self.dept + '/' + self.station 
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_pub)


    def activate_service(self):
        self.motor.turn_on()
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())
        
    def deactivate_service(self):
        self.motor.turn_off()
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