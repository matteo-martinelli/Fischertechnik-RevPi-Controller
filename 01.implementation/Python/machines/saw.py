#!/usr/bin/env python

"""
saw.py: Saw class

This class is composed by the following objects: 
    1. single activation motor O_4; 
"""

from components.single_motion_actuator import SingleMotionActuator


class Saw(object):
    """Saw class for saw objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        #self.rpi = rpi
        # Class actuators
        self.motor = \
            SingleMotionActuator(rpi, 'conveyor motor', 4)
        self.prod_under_saw = False
        self.process_completed = False


    def activate_saw(self) -> None:
        self.motor.turn_on()
        
    def deactivate_saw(self) -> None:
        self.motor.turn_off()
    
    def get_saw_state(self) -> str: 
        if (self.motor.getState() == True):
            return 'on'
        else: 
            return 'off'
