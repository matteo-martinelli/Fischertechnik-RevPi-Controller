#!/usr/bin/env python

"""
turntable_carrier_conf.py: TurntableCarrierConf class

Contains and represents the turntable carrier configuration
"""


from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json

class TurntableCarrierConf(object):
    def __init__(self, turntable_carrier_speed: int):
        self._turntable_carrier_speed = turntable_carrier_speed
        
    @property
    def turntable_carrier_speed(self): 
        return self._turntable_carrier_speed
    
    @turntable_carrier_speed.setter
    def turntable_carrier_speed(self, value: int): 
        self._turntable_carrier_speed = value
