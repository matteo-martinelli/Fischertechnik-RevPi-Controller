#!/usr/bin/env python

"""
saw_station.py: SawStation class

This class is composed by the following objects: 
    1. single activation motor O_4; 
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from datetime import datetime
import time
import json
import logging

from machines.configurations.saw_station_conf import SawStationConf
from mqtt_conf_listener import MqttConfListener

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs

class SawStation(object):
    """Saw class for saw objects."""
    def __init__(self, rpi, dept: str, station:str, saw_motor_act_pin: int, 
                 mqtt_publisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')
        
        # Class fields
        self._dept = dept
        self._station = station
        self._motor_state = False
        self._prod_under_saw = False
        self._process_completed = False
        
        self.configuration = SawStationConf(DefaultStationsConfigs.\
                                            SAW_PROCESSING_TIME)

        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station

        self.mqtt_conf_listener = MqttConfListener('multiproc_dept/saw-station/conf', self.configuration.__class__)
        self.mqtt_conf_listener.open_connection()
        self.read_conf()
       
        # Class actuators
        # pin 4
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', 
                                      saw_motor_act_pin, self.topic, 
                                      mqtt_publisher)
        # Initialising class fields
        self.read_all_actuators()


    ## Getters
    # Class fields
    @property
    def dept(self) -> str: 
        return self._dept
    
    @property
    def station(self) -> str: 
        return self._station
    
    @property
    def prod_under_saw(self) -> bool: 
        return self._prod_under_saw

    @property
    def process_completed(self) -> bool: 
        return self._process_completed

    # Actuator
    @property
    def motor_state(self) -> bool:
        return self._motor_state

    ## Setters ##
    @dept.setter
    def dept(self, value: str) -> None: 
        self._dept = value
    
    @station.setter
    def station(self, value: str) -> None: 
        self._station = value

    @prod_under_saw.setter
    def prod_under_saw(self, value: bool) -> None: 
        if(value != self._prod_under_saw):
            self._prod_under_saw = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if (value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    # Actuator
    @motor_state.setter
    def motor_state(self) -> None: 
        value = self.motor.state
        if (value != self._motor_state):
            self._motor_state = value

    # Class Methods
    def activate_saw(self) -> None: 
        if(self.motor.state == False):
            self.motor.turn_on()
            self._motor_state = True
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    

    def deactivate_saw(self) -> None: 
        if(self.motor.state == True):
            self.motor.turn_off()
            self._motor_state = False
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def processing(self, proc_time) -> None: 
        if(self.motor.state == False):
            self.activate_saw()
            self.logger.info('saw activated')
            # Time in seconds
            time.sleep(proc_time)
            self.deactivate_saw()
            self.logger.info('saw deactivated')
            self.process_completed = True

    def deactivate_station(self) -> None: 
        self.motor.turn_off()
        self._motor_state = False
        self._prod_under_saw = False
        self._process_completed = False
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    # Reading underlying sensors/actuators
    def read_motor_state(self) -> None: 
        value = self.motor.read_state()
        if (value != self._motor_state):
            self._motor_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())

    def read_all_actuators(self) -> None: 
        self.read_motor_state()

    # MQTT 
    def read_conf(self) -> None: 
        saw_proc_time_conf = self.mqtt_conf_listener.configuration 
        if (saw_proc_time_conf != self.configuration.saw_processing_time 
            and saw_proc_time_conf != None):
            self.configuration = saw_proc_time_conf
            self.logger.info('New configuration received for saw station '
                             'process time {}'\
                             .format(self.configuration.saw_proc_time_conf))
        else: 
            self.logger.info('No conf updated, proceeding with the last '
                             'configuration {} for'.format(self.station))

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
            'prod-on-carrier': self._prod_under_saw,
            'proc-completed': self._process_completed,
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
