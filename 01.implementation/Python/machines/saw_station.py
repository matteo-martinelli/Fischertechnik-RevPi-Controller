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
        # Class descriptive fields
        self.dept = dept
        self.station = station
        #self.state = False     # Helpful to track the 'idle' or 'working'state of a machine?
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor motor', 
                                      saw_motor_act_pin, self.topic, 
                                      mqtt_publisher)        # 4
        # Class virtual sensors
        self.prod_under_saw = False
        self.process_completed = False


    # Setters
    #def set_state(self) -> bool:
    #    self.state = self.motor.get_state()
    
    def set_prod_under_saw(self, value: bool) -> None: 
        self.prod_under_saw = value
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def set_process_completed(self, value: bool) -> None: 
        self.process_completed = value
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    # Getters
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station
    
    #def get_state(self) -> bool: 
    #    return self.state

    def get_prod_under_saw(self) -> bool: 
        return self.prod_under_saw

    def get_process_completed(self) -> bool: 
        return self.process_completed

    # Class Methods
    def activate_saw(self) -> None: 
        self.motor.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_saw(self) -> None: 
        self.motor.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_station(self) -> None: 
        self.motor.turn_off()
        self.set_prod_under_saw(False)
        self.set_process_completed(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    # MQTT 
    def to_dto(self):

        timestamp = time.time()
        current_moment = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

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
