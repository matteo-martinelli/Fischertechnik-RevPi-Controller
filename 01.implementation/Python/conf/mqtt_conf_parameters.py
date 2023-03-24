#!/usr/bin/env python

"""
mqtt_conf_parameter.py: MqttConfiguratorParameter class

Stores the mqtt broker connection global variables
"""

class MqttConfiguratorParameter(object):
    BROKER_ADDRESS = '192.168.137.125'
    BROKER_PORT = 1883
    MQTT_USER = 'put here the user'
    MQTT_PW = 'put here the pw'
    MQTT_BASIC_TOPIC = '/iot/user{0}'.format(MQTT_USER)    
