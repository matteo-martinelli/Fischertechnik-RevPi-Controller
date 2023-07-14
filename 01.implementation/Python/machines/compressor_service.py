#!/usr/bin/env python

"""
compressor_service.py: CompressorService class

For following pins: 
O_10: compressor.
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from datetime import datetime
import time
import json

from machines.configurations.compressor_service_conf import CompressorServiceConf
from mqtt_conf_listener import MqttConfListener

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs


class CompressorService(object):
    """Compressor class for compressor objects."""
    def __init__(self, rpi, dept: str, station: str, motor_act_pin: int, 
                 mqtt_pub):
        # Class descriptive fields
        self._dept = dept
        self._station = station
        self._motor_state = False

        self.configuration = CompressorServiceConf(DefaultStationsConfigs.\
                                                   COMPRESSOR_BEHAVIOUR)        
        
        # MQTT
        self.mqtt_pub = mqtt_pub
        self.topic = self._dept + '/' + self._station 
        
        self.mqtt_conf_listener = MqttConfListener('multiproc_dept/compressor-service/conf', self.configuration.__class__)        
        self.mqtt_conf_listener.open_connection()
        self.read_conf()
        
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
    def activate_service(self):
        self.motor.turn_on()
        self._motor_state = True
        print('compressor activated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())
        
    def deactivate_service(self):
        self.motor.turn_off()
        self._motor_state = False
        print('compressor deactivated')
        self.mqtt_pub.publish_telemetry_data(self.topic, self.to_json())

    # Reading underlying sensors/actuators
    def read_motor_state(self) -> None: 
        value = self.motor.state
        if(value != self._motor_state):
            self._motor_state = value
            self.mqtt_pub.publish_telemetry_data(self.topic, \
                                                       self.to_json())

    def read_all_actuators(self) -> None: 
        self.read_motor_state
    
    # MQTT 
    def read_conf(self) -> None: 
        compressor_behaviour_conf = self.mqtt_conf_listener.configuration 
        if (compressor_behaviour_conf != self.configuration.compressor_behaviour 
            and compressor_behaviour_conf != None):
            self.configuration = compressor_behaviour_conf
            print('New configuration received for compressor service'\
                  'behaviour', self.configuration.compressor_behaviour)
        else: 
            print('No conf updated, proceeding with the last configuration'\
                  'for', self.station)
    
    def to_dto(self):
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

    def to_json(self):
        return json.dumps(self.to_dto())