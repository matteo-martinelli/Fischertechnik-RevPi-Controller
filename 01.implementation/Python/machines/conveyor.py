#!/usr/bin/env python

"""
conveyor_carrier.py: Conveyor class

This class is composed by the following objects: 
    1. single activation motor O_3; 
    2. light barrier sensor I_3;
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from components.revpi_light_barrier import RevPiLightBarrier


class Conveyor(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, rpi):
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor motor', 3)
        # Class sensors
        self.light_barrier = \
            RevPiLightBarrier(rpi, 'conveyor light barrier', 3)
        # Class virtual sensors
        self.prod_on_conveyor = False
        self.process_completed = False


    def move_to_the_exit(self) -> None:
        while (self.light_barrier.get_state() != False):
            self.motor.turn_on()
        self.motor.turn_off()

    """
    def activate_carrier(self) -> None:
        self.motor.turn_on()

    def deactivate_carrier(self) -> None:
        self.motor.turn_off()
    
    def get_ligth_barrier_state(self) -> str: 
        if (self.light_barrier.getState() == True):
            return 'free'
        else: 
            return 'occupied'
    """
