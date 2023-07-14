#!/usr/bin/env python

"""
oven_station_conf.py: OvenStationConf class

Contains and represents the oven station configuration
"""


from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json

class OvenStationConf(object):
    def __init__(self, oven_processing_time: int):
        self._oven_processing_time = oven_processing_time
        
    @property
    def oven_processing_time(self): 
        return self._oven_processing_time
    
    @oven_processing_time.setter
    def oven_processing_time(self, value: int): 
        self._oven_processing_time = value
