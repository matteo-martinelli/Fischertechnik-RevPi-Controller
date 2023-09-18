#!/usr/bin/env python

"""
mqtt_conf_pub.py: mqtt_publisher testing file

Published the mutliproc_dept configuration into the MQTT broker
"""

import logging
from mqtt_publisher import MqttPublisher


logger = logging.getLogger('mqtt_conf_pub_test logger')
logging.basicConfig(level = logging.INFO)
mqtt_publisher = MqttPublisher()

logger.info("Setting needed topics where to put configurations")
dept_conf_topic = 'multiproc_dept/conf'
compressor_conf_topic = 'multiproc_dept/compressor-service/conf'
oven_station_conf_topic = 'multiproc_dept/oven-station/conf'
vacuum_carrier_conf_topic = 'multiproc_dept/vacuum-carrier/conf'
turntable_carrier_conf_topic = 'multiproc_dept/turntable-carrier/conf'
saw_station_conf_topic = 'multiproc_dept/saw-station/conf'
conveyor_carrier_conf_topic = 'multiproc_dept/conveyor-carrier/conf'
logger.info('Topics set')

dept_conf_alternative = \
    '{"__multiproc_dept_conf__": true,\
        "pieces_to_produce": 1,\
        "compressor_behaviour": "always_on",\
        "oven_processing_time": 3,\
        "saw_processing_time": 2,\
        "vacuum_carrier_speed_pwm": 1,\
        "turntable_carrier_speed_pwm": 1\
    }'

logger.info('Setting JSONs to be published in set topics as configurations')
dept_conf = \
    '{"pieces_to_produce": 4,\
        "compressor_behaviour": "always_on",\
        "oven_processing_time": 3,\
        "saw_processing_time": 2,\
        "vacuum_carrier_speed_pwm": 1,\
        "turntable_carrier_speed_pwm": 1\
    }'
compressor_conf = '{"motor_behaviour": "always_on"}'
oven_station_conf = '{"oven_processing_time": 3}'
vacuum_carrier_conf = '{"vacuum_carrier_speed": "High"}'
turntable_carrier_conf = '{"turntable_carrier_speed_pwm": 1}'
saw_conf = '{"saw_processing_time": 2}'
conveyor_conf = '{"none"}'
logger.info('JSONs set')

logger.info('Opening MQTT connection ... ')
mqtt_publisher.open_connection()

logger.info('Publishing MQTT data ...')
mqtt_publisher.publish_telemetry_data(dept_conf_topic,
                                      dept_conf, True)
mqtt_publisher.publish_telemetry_data(compressor_conf_topic,
                                      compressor_conf, True)
mqtt_publisher.publish_telemetry_data(oven_station_conf_topic, 
                                      oven_station_conf, True)
mqtt_publisher.publish_telemetry_data(vacuum_carrier_conf_topic, 
                                      vacuum_carrier_conf, True)
mqtt_publisher.publish_telemetry_data(turntable_carrier_conf_topic,
                                      turntable_carrier_conf, True)
mqtt_publisher.publish_telemetry_data(saw_station_conf_topic,
                                      saw_conf, True)
mqtt_publisher.publish_telemetry_data(conveyor_carrier_conf_topic,
                                      conveyor_conf, True)

logger.info('Closing connection ...')
mqtt_publisher.close_connection()

logger.info('Connection closed, configurations published')
