from mqtt_publisher import MqttPublisher

mqtt_publisher = MqttPublisher()

my_topic = 'multiproc_dept/dept_conf'
my_json2 = '{"__multiproc_dept_conf__": true,\
            "pieces_to_produce": 1,\
            "compressor_behaviour": "always_on",\
            "oven_processing_time": 3,\
            "saw_processing_time": 2,\
            "vacuum_carrier_speed_pwm": 1,\
            "turntable_carrier_speed_pwm": 1\
        }'

my_json = '{"pieces_to_produce": 1,\
            "compressor_behaviour": "always_on",\
            "oven_processing_time": 3,\
            "saw_processing_time": 2,\
            "vacuum_carrier_speed_pwm": 1,\
            "turntable_carrier_speed_pwm": 1\
        }'

mqtt_publisher.open_connection()
mqtt_publisher.publish_telemetry_data(my_topic, my_json)
mqtt_publisher.close_connection()