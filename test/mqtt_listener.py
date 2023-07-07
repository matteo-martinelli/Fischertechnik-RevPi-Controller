#!/usr/bin/env python

"""
mqtt_listener.py: MqttListener class
"""


import time
import paho.mqtt.client as mqtt
import json

"""Mqtt publisher class to publish mqtt topics."""

def on_connect(client , userdata , flags , rc):
    print('Mqtt listener client connected with result code ' + str(rc))
    #subscribe_to_listen_topics('multiproc_dept/dept_conf', my_client)
    #target_topic = 'user:{0}/{1}/'.format('dept_manager', topic)
    topic = 'user:dept_manager/multiproc_dept/dept_conf/'
    client.subscribe(topic)
    print('Trying to subscribe to ', topic)

def on_message(client, userdata, msg):
    print('Received a message: ', msg)
    decoded_message = str(msg.payload.decode("utf-8"))
    json_message = json.loads(decoded_message)
    print(json_message)

def on_subscribe(client, userdata, mid, granted_qos):
    print('Subscribed with mid ', mid)
    
def close_connection(client):
    client.loop_stop()
    print('Mqtt listener client Loop stopped')


my_client = mqtt.Client(client_id='test_listener')
print('starting' + str(my_client))
my_client.on_connect = on_connect
my_client.on_message = on_message
my_client.on_subscribe = on_subscribe
my_client.connect('10.0.0.6', 1883)
my_client.loop_start()
time.sleep(2)
close_connection(my_client)
