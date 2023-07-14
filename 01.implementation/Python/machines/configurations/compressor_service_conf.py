#!/usr/bin/env python

"""
cmpressor_service_conf.py: CompressorServiceConf class

Contains and represents the compressor service configuration
"""


from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json

class CompressorServiceConf(object):
    def __init__(self, compressor_behaviour: str):
        self._compressor_behaviour = compressor_behaviour
        
    @property
    def compressor_behaviour(self): 
        return self._compressor_behaviour
    
    @compressor_behaviour.setter
    def oven_processing_time(self, value: str): 
        self._compressor_behaviour = value
