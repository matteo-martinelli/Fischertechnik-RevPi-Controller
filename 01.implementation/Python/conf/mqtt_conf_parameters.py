#!/usr/bin/env python

"""
mqtt_conf_parameter.py: MqttConfiguratorParameter class

Stores the mqtt broker connection global variables
"""


class MqttConfiguratorParameter(object):
    BROKER_ADDRESS = '192.168.137.125'
    BROKER_PORT = 1883
    MQTT_USER = 'dept_manager'
    MQTT_PW = 'put here the pw'
    MQTT_BASIC_TOPIC = '/user_{0}'.format(MQTT_USER)    

    ACTIVE_MQTT = True
    PRINT_PUBLISHED_DATA = True
    DEPT_TOPIC = 'multiproc_dept'
    OVEN_STATION_TOPIC = 'oven-station'
    VACUUM_CARRIER_TOPIC = 'vacuum-carrier'
    TURNTABLE_CARRIER_TOPIC = 'turntable-carrier' 
    SAW_STATION_TOPIC = 'saw-station'
    CONVEYOR_CARRIER_TOPIC = 'conveyor-carrier'