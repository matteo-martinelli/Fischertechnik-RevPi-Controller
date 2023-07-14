#!/usr/bin/env python

"""
mqtt_listener.py: MqttListener class
"""


import traceback
from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json
import logging


class MqttConfListener(object):
    """Mqtt publisher class to publish mqtt topics."""
    def __init__(self, topic_to_subscribe, conf_class):
        
        self.logger = logging.getLogger('multiproc_dept_logger')
        
        self.mqtt_client = mqtt.Client()
        self.topic_to_subscribe = topic_to_subscribe
        self.conf_class = conf_class
        self.configuration = None

    def on_connect(self, client , userdata , flags , rc):
        self.logger.info('Mqtt listener client connected with result code {}'\
                         .format(str(rc)))
        self.subscribe_multiproc_dept_configuration(self.topic_to_subscribe)

    def on_message(self, client, userdata, msg):
        decoded_message = str(msg.payload.decode("utf-8"))
        json_message = json.loads(decoded_message)
        self.logger.info('Received a conf message for {}'\
                         .format(self.conf_class))
        self.manually_decode_conf(json_message)
        # TODO: check if the message has the needed format

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.info('Succesfully subscribed with mid {}'.format(mid))

    def open_connection(self):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.on_subscribe = self.on_subscribe

        #mqtt_configured_user = MqttConfiguratorParameter.MQTT_USER
        #mqtt_configured_pw = MqttConfiguratorParameter.MQTT_PW
        mqtt_configured_address = MqttConfiguratorParameter.BROKER_ADDRESS
        mqtt_configured_port = MqttConfiguratorParameter.BROKER_PORT

        #mqtt_client.username_pw_set(mqtt_configured_user,mqtt_configured_pw)
        self.mqtt_client.connect(mqtt_configured_address, mqtt_configured_port)
        
        self.mqtt_client.loop_start()
        
    def close_connection(self):
        self.mqtt_client.loop_stop()
        self.logger.info('Mqtt listener client Loop stopped')

    # TODO: set the configuration retain flag
    def subscribe_multiproc_dept_configuration(self, topic):
        if (MqttConfiguratorParameter.ACTIVE_MQTT == True):
            mqtt_configured_user = MqttConfiguratorParameter.MQTT_USER
            target_topic = 'user:{0}/{1}/'.format(mqtt_configured_user, topic)
            self.mqtt_client.subscribe(target_topic)
            self.logger.info('Subscribing tentative to {}'\
                             .format(target_topic, ' ...'))

    def manually_decode_conf(self, conf_dict: dict):
        try:
            multiproc_conf = self.conf_class
            self.logger.info('Decoding ...')
            for key in conf_dict:
                setattr(multiproc_conf, key, conf_dict[key])
            
            self.configuration = self.conf_class(multiproc_conf) 
            self.logger.info('Received MQTT configuration saved for {}'\
                             .format(self.conf_class))
        except Exception as exc: 
            self.logger.info('an error occured! Error: {}'.format(exc))
            # printing stack trace
            self.logger.info(traceback.print_exc())
