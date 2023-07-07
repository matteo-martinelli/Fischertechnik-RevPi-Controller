#!/usr/bin/env python

"""
multiproc_dept_conf.py: MultiProcDeptConf class
"""


from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json

class MultiProcDeptConf(object):
    """Configuration class storing information about the department 
    configuration setting.    
    """

    def __init__(self, pieces_to_produce=0, compressor_behaviour="always_on", 
                 oven_processing_time=0, saw_processing_time=0, 
                 vacuum_carrier_speed=0, turntable_carrier_speed=0):
        self.pieces_to_produce = pieces_to_produce
        self.compressor_behaviour = compressor_behaviour
        self.oven_processing_time = oven_processing_time
        self.saw_processing_time = saw_processing_time
        self.vacuum_carrier_speed = vacuum_carrier_speed
        self.turntable_carrier_speed = turntable_carrier_speed

        @property
        def pieces_to_produce(self):
            return self.pieces_to_produce
        
        @pieces_to_produce.setter
        def pieces_to_produce(self, value: int):
            self.pieces_to_produce = value
        
        @property
        def compressor_behaviour(self): 
            return compressor_behaviour
        
        @compressor_behaviour.setter
        def compressor_behaviour(self, value: bool):
            self.compressor_behaviour = compressor_behaviour

        @property
        def oven_processing_time(self): 
            return self.oven_processing_time
        
        @compressor_behaviour.setter
        def oven_processing_time(self, value: int): 
            self.oven_processing_time = value

        @property
        def saw_processing_time(self):
            return self.saw_processing_time
        
        @saw_processing_time.setter
        def saw_processing_time(self, value: int):
            self.saw_processing_time = value

        @property
        def vacuum_carrier_speed(self):
            return self.vacuum_carrier_speed
        
        @vacuum_carrier_speed.setter
        def vacuum_carrier_speed(self, value: int):
            self.vacuum_carrier_speed = value

        @property
        def turntable_carrier_speed(self):
            return self.turntable_carrier_speed
        
        @turntable_carrier_speed.setter
        def turntable_carrier_speed(self, value: int):
            self.turntable_carrier_speed = value
