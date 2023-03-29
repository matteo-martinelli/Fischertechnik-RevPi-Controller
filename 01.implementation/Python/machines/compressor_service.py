#!/usr/bin/env python

"""
compressor_service.py: CompressorService class

For following pins: 
O_10: compressor.
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
import json


class CompressorService(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, motor_act_pin: int, mqtt_pub):
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'compressor-motor', motor_act_pin)
        #self.name = pass
        #self.dept = pass # TODO: will represent the main topic

        self.topic = 'proc_dept/services/compressor/telemetry'
        self.mqtt_pub = mqtt_pub


    def activate(self):
        self.motor.turn_on()
        self.mqtt_pub.publish_telemetry_data(self.topic, self.motor.to_json())
        #print(self.motor.to_json())

    def deactivate(self):
        self.motor.turn_off()
        self.mqtt_pub.publish_telemetry_data(self.topic, self.motor.to_json())
