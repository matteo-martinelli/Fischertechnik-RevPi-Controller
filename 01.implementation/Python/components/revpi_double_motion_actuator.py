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
import json


class RevPiDoubleMotionActuator(GenericRevPiActuator):
    """Double Activation Motor class for double motor actuated objects."""
    def __init__(self, rpi, name: str, pin_A: int, pin_B: int):
        super().__init__(rpi)
        self.name = name
        self.pin_tuple = (pin_A, pin_B)
        self.get_state()     # First reading of the actual state


    # Getters
    def get_state(self) -> None:
        state_A = self.rpi.io['O_' + str(self.pin_tuple[0])].value
        state_B = self.rpi.io['O_' + str(self.pin_tuple[1])].value
        self.state = (state_A, state_B)
        return self. state
    # Class Methods
    def turn_on(self, activation_pin: int):
        for i in range(len(self.pin_tuple)):
            if self.pin_tuple[i] == activation_pin: 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = True
                self.state = True
            else: 
                self.rpi.io['O_' + str(self.pin_tuple[i])].value = False
    
    def turn_off(self) -> None:
        self.state = False
        for i in range(len(self.pin_tuple)):
            self.rpi.io['O_' + str(self.pin_tuple[i])].value = self.state

    # MQTT 
    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'pins': self.pin_tuple,
            'state': self.state,
            'timestamp': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())