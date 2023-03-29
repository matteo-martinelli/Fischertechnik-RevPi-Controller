#!/usr/bin/env python

"""
saw_station.py: SawStation class

This class is composed by the following objects: 
    1. single activation motor O_4; 
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator


class SawStation(object):
    """Saw class for saw objects."""
    def __init__(self, rpi, dept: str, station:str, saw_motor_act_pin: int, 
                 mqtt_publisher):
        # Class descriptive fields
        self.dept = dept
        self.station = station
        self.state = False
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor motor', 
                                      saw_motor_act_pin)        # 4
        # Class virtual sensors
        self.prod_under_saw = False
        self.process_completed = False
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = 'put/some/topic'   # TODO: eventually change it


    # Setters
    def set_state(self) -> bool:
        self.state = self.motor.get_state()
    
    def set_prod_under_saw(self, value: bool) -> None: 
        self.prod_under_saw = value

    def set_process_completed(self, value: bool) -> None: 
        self.process_completed = value
    
    # Getters
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station
    
    def get_state(self) -> bool: 
        return self.state

    def get_prod_under_saw(self) -> bool: 
        return self.prod_under_saw

    def get_process_completed(self) -> bool: 
        return self.process_completed

    # Class Methods
    def activate(self) -> None: 
        self.motor.turn_on()

    def deactivate(self) -> None: 
        self.motor.turn_off()
