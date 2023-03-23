#!/usr/bin/env python

"""
single_motion_actuator.py: SingleMotionActuator class

For following pins: 
O_3: conveyor belt;
O_4: saw; 
O_9: processing light;
O_10: compressor.
"""

from components.basic_components.generic_actuator import GenericActuator


class SingleMotionActuator(GenericActuator):
    """Single Motion Actuator class for single motion actuated objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi)
        self.name = name
        self.pin_tuple = (pin,)
        self.get_state()


    def get_name(self) -> str:
        return self.name

    def get_state(self) -> bool: 
        self.state = self.rpi.io['O_'+ str(self.pin_tuple[0])].value
        return self.state
    
    def turn_on(self) -> None:
        # TODO: deve chiamare turn_on() del pin della classe padre 
        self.state = True
        self.rpi.io['O_'+ str(self.pin_tuple[0])].value = self.state
