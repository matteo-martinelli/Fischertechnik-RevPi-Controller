from mqtt_publisher import MqttPublisher
import json

mqtt_publisher = MqttPublisher()

dept_conf_topic = 'multiproc_dept/conf'
compressor_conf_topic = 'multiproc_dept/compressor-service/conf'
oven_station_conf_topic = 'multiproc_dept/oven-station/conf'
vacuum_carrier_conf_topic = 'multiproc_dept/vacuum-carrier/conf'
turntable_carrier_conf_topic = 'multiproc_dept/turntable-carrier/conf'
saw_station_conf_topic = 'multiproc_dept/saw-station/conf'
conveyor_carrier_conf_topic = 'multiproc_dept/conveyor-carrier/conf'


dept_conf_alternative = \
    '{"__multiproc_dept_conf__": true,\
        "pieces_to_produce": 1,\
        "compressor_behaviour": "always_on",\
        "oven_processing_time": 3,\
        "saw_processing_time": 2,\
        "vacuum_carrier_speed_pwm": 1,\
        "turntable_carrier_speed_pwm": 1\
    }'

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
vacuum_carrier_conf = '{"vacuum_carrier_speed_pwm": 1}'
turntable_carrier_conf = '{"turntable_carrier_speed_pwm": 1}'
saw_conf = '{"saw_processing_time": 2}'
conveyor_conf = '{"none"}'

mqtt_publisher.open_connection()

mqtt_publisher.publish_telemetry_data(dept_conf_topic,dept_conf)
mqtt_publisher.publish_telemetry_data(compressor_conf_topic,compressor_conf)
mqtt_publisher.publish_telemetry_data(oven_station_conf_topic, oven_station_conf)
mqtt_publisher.publish_telemetry_data(vacuum_carrier_conf_topic, vacuum_carrier_conf)
mqtt_publisher.publish_telemetry_data(turntable_carrier_conf_topic,turntable_carrier_conf)
mqtt_publisher.publish_telemetry_data(saw_station_conf_topic,saw_conf)
mqtt_publisher.publish_telemetry_data(conveyor_carrier_conf_topic,conveyor_conf)

mqtt_publisher.close_connection()