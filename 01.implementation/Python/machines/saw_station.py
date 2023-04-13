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


class SawStation(object):
    """Saw class for saw objects."""
    def __init__(self, rpi, dept: str, station:str, saw_motor_act_pin: int, 
                 mqtt_publisher):
        # Class fields
        self.dept = dept
        self.station = station
        self.motor_state = False
        self.prod_under_saw = False
        self.process_completed = False
        
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        # Class actuators
        # pin 4
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', 
                                      saw_motor_act_pin, self.topic, 
                                      mqtt_publisher)
        # Initialising class fields
        self.read_actuators()
        self.set_prod_under_saw(False)
        self.set_process_completed(False)

    # Read all sensors and actuators
    def read_actuators(self) -> None: 
        self.set_motor_state()
        
    ## Setters ##
    # Actuator
    def set_motor_state(self) -> None: 
        value = self.motor.get_state()
        if (value != self.motor_state):
            self.motor_state = value

    def set_prod_under_saw(self, value: bool) -> None: 
        if(value != self.get_prod_under_saw()):
            self.prod_under_saw = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def set_process_completed(self, value: bool) -> None: 
        if (value != self.get_process_completed()):
            self.process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    ## Getters ##
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station
    
    # Actuator
    def get_motor_state(self) -> bool:
        return self.motor_state
    
    def get_prod_under_saw(self) -> bool: 
        return self.prod_under_saw

    def get_process_completed(self) -> bool: 
        return self.process_completed

    # Class Methods
    def activate_saw(self) -> None: 
        if(self.motor.get_state() == False):
            self.motor.turn_on()
            self.set_motor_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def deactivate_saw(self) -> None: 
        if(self.motor.get_state() == True):
            self.motor.turn_off()
            self.set_motor_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def deactivate_station(self) -> None: 
        self.motor.turn_off()
        self.set_motor_state()
        self.set_prod_under_saw(False)
        self.set_process_completed(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'motor': self.motor.get_state(),
            'prod-on-carrier': self.get_prod_under_saw(),
            'proc-completed': self.get_process_completed(),
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
