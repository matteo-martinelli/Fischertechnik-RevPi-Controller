#!/usr/bin/env python

"""
conveyor_carrier.py: ConveyorCarrier class

This class is composed by the following objects: 
    1. single activation motor O_3; 
    2. light barrier sensor I_3;
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from components.revpi_light_barrier_sensor import RevPiLightBarrierSensor
from datetime import datetime
import time
import json


class ConveyorCarrier(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, rpi, dept: str, station: str, motor_act_pin: int, 
                 barrier_sens_pin: int, mqtt_publisher):
        # Class fields
        self.dept = dept
        self.station = station
        self.motor_state = False
        self.light_barrier_state = False
        self.prod_on_conveyor = False
        self.process_completed = False
        
        #self.last_motor_state = False
        #self.last_light_barrier_state = False
        #self.last_prod_on_conveyor = False
        #self.last_process_completed = False
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        # Class actuators
        # pin 3
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_publisher)
        # pin 3
        self.light_barrier = \
            RevPiLightBarrierSensor(rpi, 'light-barrier', 
                                    barrier_sens_pin, self.topic, 
                                    self.mqtt_publisher)
        self.read_sensors()
        self.read_actuators()

    # Read all sensors and actuators
    def read_sensors(self) -> None: 
        self.set_light_barrier_state()
    
    def read_actuators(self) -> None: 
        self.set_motor_state()
    
    ## Setters ##
    # Actuator
    # When necessary pub
    def set_motor_state(self) -> None: 
        value = self.motor.get_state()
        if (value != self.motor_state):
            self.motor_state = value

    # Sensor
    # Polling pub
    def set_light_barrier_state(self) -> None: 
        value = self.light_barrier.get_state()
        if (value != self.light_barrier_state):
            if (value == True):
                self.light_barrier_state = True
            else:
                self.light_barrier_state = False
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    # TODO: add "if flag = True, then publish"
    def set_prod_on_conveyor(self, value: bool) -> None: 
        if(value != self.get_prod_on_conveyor()):
            self.prod_on_conveyor = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    # TODO: add "if flag = True, then publish"
    def set_process_completed(self, value: bool) -> None: 
        if(value != self.get_process_completed()):
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

    # Sensor
    def get_light_barrier_state(self) -> bool:
        return self.light_barrier_state

    def get_prod_on_conveyor(self) -> bool: 
        return self.prod_on_conveyor

    def get_process_completed(self) -> bool: 
        return self.process_completed

    # Class Methods
    def move_to_the_exit(self) -> None:
        self.motor.turn_on()
        self.set_motor_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        
        # Wait until a product reaches the light_barrier sensor
        while (self.light_barrier.get_state() != False):
            pass

        self.motor.turn_off()
        self.set_motor_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.set_motor_state()
        
        self.set_prod_on_conveyor(False)
        self.set_process_completed(False)
        # MQTT Publish
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'conveyor_motor': self.get_motor_state(),
            'light-barrier': self.get_light_barrier_state(),
            'prod_on_conv:': self.get_prod_on_conveyor(),
            'process_complete:': self.get_process_completed(),
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
