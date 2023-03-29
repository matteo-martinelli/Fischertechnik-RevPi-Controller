#!/usr/bin/env python

"""
saw_station.py: SawStation class

This class is composed by the following objects: 
    1. single activation motor O_4; 
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator


class SawStation(object):
    """Saw class for saw objects."""
    def __init__(self, rpi, saw_motor_act_pin: int):
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor motor', 
                                      saw_motor_act_pin)        # 4
        self.prod_under_saw = False
        self.process_completed = False
