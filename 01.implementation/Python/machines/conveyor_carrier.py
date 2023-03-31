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
import json


class ConveyorCarrier(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, rpi, dept: str, station: str, motor_act_pin: int, 
                 barrier_sens_pin: int, mqtt_publisher):
        # Class descriptive fields
        self.dept = dept
        self.station = station
        #self.state = self.motor.get_state()    # Helpful to track the 'idle' or 'working'state of a machine?
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor-motor', motor_act_pin, 
                                      self.topic, mqtt_publisher) # 3
        self.light_barrier = \
            RevPiLightBarrierSensor(rpi, 'conveyor-light-barrier', 
                                    barrier_sens_pin)                       # 3
        # Class virtual sensors
        self.prod_on_conveyor = False
        self.process_completed = False


    # Setters
    def set_prod_on_conveyor(self, value: bool) -> None: 
        self.prod_on_conveyor = value
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

    def get_light_barrier_state(self) -> bool: 
        return self.light_barrier.get_state()

    def get_prod_on_conveyor(self) -> bool: 
        return self.prod_on_conveyor

    def get_process_completed(self) -> bool: 
        return self.process_completed

    # Class Methods
    def move_to_the_exit(self) -> None:
        # Counter set to publish only 1 time through the cycle
        counter = 0
        while (self.light_barrier.get_state() != False):
            self.motor.turn_on()
            
            if (counter == 0): 
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
                counter += 1
        
        self.motor.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.set_prod_on_conveyor(False)
        self.set_process_completed(False)
        # MQTT Publish
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'conveyor_motor': self.motor.get_state(),
            'light-barrier': self.light_barrier.get_state(),
            'prod_on_conv:': self.get_prod_on_conveyor(),
            'process_complete:': self.get_process_completed(),
            
            'timestamp': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
