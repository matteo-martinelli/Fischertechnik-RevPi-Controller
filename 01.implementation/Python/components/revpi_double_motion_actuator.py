#!/usr/bin/env python

"""
double_motion_actuator.py: DoubleMotionActuator class

For following pins: 
O_1: turntable clockwise
O_2: turntable counter-clockwise
O_5: oven carrier inside
O_6: oven carrier outside
O_7: vacuum carrier towards oven
O_8: vacuum carrier towards turntable
"""

from components.basic_components.generic_revpi_actuator import GenericRevPiActuator
from datetime import datetime
import time
import json


class RevPiDoubleMotionActuator(GenericRevPiActuator):
    """Double Activation Motor class for double motor actuated objects."""
    def __init__(self, rpi, name: str, pin_A: int, pin_B: 
                 int, parent_topic: str, mqtt_publisher):
        super().__init__(rpi)
        # MQTT
        self.topic = parent_topic + '/actuators/' + name
        self.mqtt_publisher = mqtt_publisher
        # Class fields
        self.name = name
        self.pin_tuple = (pin_A, pin_B)
        # Fields init
        self.get_state()


    # Getters
    def get_state(self) -> None:
        state_A = self.rpi.io['O_' + str(self.pin_tuple[0])].value
        state_B = self.rpi.io['O_' + str(self.pin_tuple[1])].value
        self.state = (state_A, state_B)
        if(self.state != self.previous_state):  # TODO: where is previous state?
            self.previous_state = self.state
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
        return self.state
    
    # Class Methods
    def turn_on(self, activation_pin: int): # TODO: write it better
        for i in range(len(self.pin_tuple)):
            if (self.pin_tuple[i] == activation_pin and 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value == False): 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = True
                #self.state = True
                #self.mqtt_publisher.publish_telemetry_data(self.topic, 
                #                                           self.to_json())
                self.get_state()
            else: 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = False
                self.get_state()
        
    def turn_off(self) -> None: # TODO: write it better
        if (self.state[0] != False or self.state[1] != False):
            self.state = (False, False)
            for i in range(len(self.pin_tuple)):
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = False
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'type': self.__class__.__name__,
            'layer': 'sensor-actuator',
            'pins': self.pin_tuple,
            'state': self.state,
            
            'timestamp': timestamp,
            'current-time': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())