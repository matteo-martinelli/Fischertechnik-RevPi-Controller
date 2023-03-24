#!/usr/bin/env python

"""
saw.py: Saw class

This class is composed by the following objects: 
    1. single activation motor O_4; 
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator


class Saw(object):
    """Saw class for saw objects."""
    def __init__(self, rpi):
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor motor', 4)
        self.prod_under_saw = False
        self.process_completed = False
