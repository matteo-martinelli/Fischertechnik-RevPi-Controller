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
import logging


class ConveyorCarrier(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, rpi, dept: str, station: str, motor_act_pin: int, 
                 barrier_sens_pin: int, mqtt_publisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')
        
        self._dept = dept
        self._station = station
        self._motor_state = False
        self._light_barrier_state = False
        self._prod_on_conveyor = False
        self._process_completed = False
        
        self.mqtt_publisher = mqtt_publisher
        self.topic = self._dept + '/' + self._station
        
        # pin 3
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_publisher)
        # pin 3
        self.light_barrier = \
            RevPiLightBarrierSensor(rpi, 'light-barrier', 
                                    barrier_sens_pin, self.topic, 
                                    self.mqtt_publisher)
        self.read_all_sensors()
        self.read_all_actuators()

    
    ## Getters
    # Class fields
    @property
    def dept(self) -> str: 
        return self._dept
    
    @property
    def station(self) -> str: 
        return self._station

    # Actuator
    @property
    def motor_state(self) -> bool:
        return self._motor_state

    # Sensor
    @property
    def light_barrier_state(self) -> bool:
        return self._light_barrier_state

    @property
    def prod_on_conveyor(self) -> bool: 
        return self._prod_on_conveyor

    @property
    def process_completed(self) -> bool: 
        return self._process_completed

    ## Setters
    @dept.setter
    def dept(self, value: str) -> None: 
        self._dept = value
    
    @station.setter
    def station(self, value: str) -> None: 
        self._station = value

    @motor_state.setter
    def motor_state(self, value: bool) -> None: 
        self._motor_state = value
    
    @light_barrier_state.setter
    def light_barrier_state(self, value: bool) -> None: 
        self._light_barrier_state = value

    @prod_on_conveyor.setter
    def prod_on_conveyor(self, value: bool) -> None: 
        if(value != self._prod_on_conveyor):
            self._prod_on_conveyor = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if(value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # Class Methods
    # Processes methods
    def move_to_the_exit(self) -> None:
        self.motor.turn_on()
        self.read_motor_state()
        self.logger.info('conveyor activated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)
        
        # Wait until a product reaches the light_barrier sensor
        while (self.light_barrier.read_state() != False):
            pass

        self.motor.turn_off()
        self.read_motor_state()
        self.logger.info('conveyor deactivated')
        self.process_completed = True
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def turn_off_all_actuators(self) -> None: 
        self.motor.turn_off()
        self.read_motor_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def reset_process_states(self) -> None: 
        self._prod_on_conveyor = False
        self._process_completed = False
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def closing_connections(self) -> None: 
        pass

    def reset_carrier(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        
    def deativate_carrier(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        #self.mqtt_conf_listener.close_connection                               -> actually not present

    # Reading underlying sensors/actuators
    def read_motor_state(self) -> None: # QUESTA E' UNA LETTURA
        value = self.motor.read_state()
        if (value != self._motor_state):
            self._motor_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic,
                                                       self.to_json(), True)

    def read_light_barrier_state(self) -> None: # QUESTA E' UNA LETTURA 
        value = self.light_barrier.read_state()
        if (value != self._light_barrier_state):
            self._light_barrier_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
    
    # Read all sensors and actuators
    def read_all_sensors(self) -> None: 
        self.read_light_barrier_state()
    
    def read_all_actuators(self) -> None: 
        self.read_motor_state()

    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'conveyor_motor': self._motor_state,
            'light-barrier': self._light_barrier_state,
            'prod_on_conv:': self._prod_on_conveyor,
            'process_complete:': self._process_completed,
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
