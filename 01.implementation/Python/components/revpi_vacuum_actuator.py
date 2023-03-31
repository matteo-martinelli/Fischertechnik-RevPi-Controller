#!/usr/bin/env python

"""
vacuum_actuator.py: VacuumActuator class

For following pins: 
O_11: vacuum gripper on carrier activation;
O_12: vacuum gripper on carrier lowering;
O_13: vacuum activated oven doors opening;
O_14: turntable vacuum pusher activation.
"""

from components.basic_components.generic_revpi_actuator import GenericRevPiActuator
from datetime import datetime
import json

class RevPiVacuumActuator(GenericRevPiActuator):
    """Vacuum Actuator class for vacuum activated objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi)
        self.name = name
        self.pin = pin
        # self.compressor = ... TODO: add compressor check


    # Getters
    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin)].value
        return self.state
    # Class Methods
    def turn_on(self) -> None: 
        self.state = True
        self.rpi.io['O_'+ str(self.pin)].value = self.state

    def turn_off(self) -> None:
        self.state = False
        self.rpi.io['O_'+ str(self.pin)].value = self.state

    # MQTT 
    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'pin': self.pin,
            'state': self.state,
            'type': self.__class__.__name__,
            'layer': 'sensor-actuator',
            
            'timestamp': current_moment 
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())