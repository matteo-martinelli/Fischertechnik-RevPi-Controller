#!/usr/bin/env python

"""
compressor_service.py: CompressorService class

For following pins: 
O_10: compressor.
"""

from mqtt.mqtt_publisher import MqttPublisher
import revpimodio2
from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from datetime import datetime
import time
import json
import logging

from machines.configurations.compressor_service_conf import CompressorServiceConf
from mqtt.mqtt_conf_listener import MqttConfListener

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs


class CompressorService(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi: revpimodio2.RevPiModIO, dept: str, station: str, 
                 motor_act_pin: int, mqtt_pub: MqttPublisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')

        # Class descriptive fields
        self._dept = dept
        self._station = station
        self._motor_state = False

        self.configuration = CompressorServiceConf(DefaultStationsConfigs.\
                                                   COMPRESSOR_BEHAVIOUR)        
        
        # MQTT
        self.mqtt_pub = mqtt_pub
        self.topic = self._dept + '/' + self._station 
        
        self.mqtt_conf_listener = \
            MqttConfListener('multiproc_dept/compressor-service/conf', 
                             self.configuration.to_object)        
        self.mqtt_conf_listener.open_connection()
        
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_pub)
        self.read_all_actuators()


    # Getters
    @property
    def dept(self) -> str: 
        return self._dept
    
    @property
    def station(self) -> str: 
        return self._station

    @property
    def motor_state(self) -> bool:
        return self._motor_state
    
    # Setters
    @dept.setter
    def dept(self, value: str) -> None: 
        self._dept = value
    
    @station.setter
    def station(self, value: str) -> None: 
        self._station = value

    @motor_state.setter
    def motor_state(self, value: bool) -> None: 
        #value = self.motor.get_state()
        if (value != self._motor_state):
            self._motor_state = value
    
    # Class methods
    def activate_service(self) -> None:
        self.motor.turn_on()
        self._motor_state = True
        self.logger.info('compressor activated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json(), True)
    
    def turn_off_all_actuators(self) -> None: 
        self.motor.turn_off()
        self._motor_state = False
        self.logger.info('compressor deactivated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json(), True)

    def close_connections(self) -> None: 
        self.mqtt_conf_listener.close_connection()

    def deactivate_service(self) -> None:
        self.turn_off_all_actuators()
        self.close_connections()

    # Reading underlying sensors/actuators
    def read_motor_state(self) -> None: 
        value = self.motor.state
        if(value != self._motor_state):
            self._motor_state = value
            self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json(), 
                                                 True)

    def read_all_actuators(self) -> None: 
        self.read_motor_state
    
    # MQTT 
    def read_conf(self) -> None: 
        new_compressor_behaviour_conf = self.mqtt_conf_listener.configuration 
        if (new_compressor_behaviour_conf != None):
            if(new_compressor_behaviour_conf.compressor_behaviour != 
               self.configuration.compressor_behaviour):
                self.logger.info('New configuration received for compressor '
                                'service behaviour - old value {}; '
                                'new value {}; overriding the whole object'\
                                .format(self.configuration\
                                        .compressor_behaviour,
                                        new_compressor_behaviour_conf\
                                        .compressor_behaviour))
                self.configuration = new_compressor_behaviour_conf
            else: 
                self.logger.info('No conf updated, proceeding with the last '
                                 'compressor_behaviour of {} for {}'\
                                 .format(self.configuration\
                                         .compressor_behaviour, 
                                         self.station))
        else: 
            self.logger.info('No conf updated, proceeding with the last '
                            'compressor_behaviour of {} for {}'\
                            .format(self.configuration.oven_processing_time, 
                                    self.station))

    def to_dto(self) -> dict:
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'motor': self.motor.state,
            
            'timestamp': timestamp,
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dto())