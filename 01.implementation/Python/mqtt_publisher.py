#!/usr/bin/env python

"""
mqtt_publisher.py: MqttPublisher class

For following pins: 
O_10: compressor.
"""

from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt

class MqttPublisher(object):
    """Mqtt publisher class to publish mqtt topics."""
    def __init__(self):
        self.mqtt_client = mqtt.Client()

    def on_connect(self, client , userdata , flags , rc):
        print('Mqtt connected with result code ' + str(rc))

    def open_connection(self):
        self.mqtt_client.on_connect = self.on_connect
        #mqtt_client.username_pw_set(MqttConfiguratorParameter.MQTT_USER,
        #                            MqttConfiguratorParameter.MQTT_PW)
        self.mqtt_client.connect(MqttConfiguratorParameter.BROKER_ADDRESS, 
                                MqttConfiguratorParameter.BROKER_PORT)
        self.mqtt_client.loop_start()

    def close_connection(self):
        self.mqtt_client.loop_stop()
        print('Mqtt Loop stopped')

    def publish_telemetry_data():
        target_topic = '{0}/{1}/'
        pass    

