#!/usr/bin/env python

"""
mqtt_publisher.py: MqttPublisher class

For following pins: 
O_10: compressor.
"""


import time
from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json

class MqttPublisher(object):
    """Mqtt publisher class to publish mqtt topics."""
    def __init__(self):
        self.mqtt_client = mqtt.Client()

    def on_connect(self, client , userdata , flags , rc):
        print('Mqtt publisher client connected with result code ' + str(rc))

    def open_connection(self):
        self.mqtt_client.on_connect = self.on_connect

        #mqtt_configured_user = MqttConfiguratorParameter.MQTT_USER
        #mqtt_configured_pw = MqttConfiguratorParameter.MQTT_PW
        mqtt_configured_address = MqttConfiguratorParameter.BROKER_ADDRESS
        mqtt_configured_port = MqttConfiguratorParameter.BROKER_PORT

        #mqtt_client.username_pw_set(mqtt_configured_user,mqtt_configured_pw)
        self.mqtt_client.connect(mqtt_configured_address, mqtt_configured_port)
        self.mqtt_client.loop_start()
        
    def close_connection(self):
        self.mqtt_client.loop_stop()
        print('Mqtt publisher client Loop stopped')

    # TODO: set the configuration retain flag
    def publish_telemetry_data(self, topic: str, target_payload: json):
        if (MqttConfiguratorParameter.ACTIVE_MQTT == True):
            mqtt_configured_user = MqttConfiguratorParameter.MQTT_USER
            target_topic = 'user:{0}/{1}/'.format(mqtt_configured_user, topic)
            #target_payload = payload.to_json()
            self.mqtt_client.publish(target_topic, target_payload, 0, True)
            #print(f"Info Published: Topic: {target_topic} Payload: {target_payload}")
