#!/usr/bin/env python

"""
oven.py: Oven class

This class is composed by the following objects: 
    1. light barrier sensor; 
    2. double actuated product carrier; 
    3. vacuum actuated oven door;
    4. inward reference switch;
    5. outward reference switch;
    6. process light. 
"""

from light_barrier import LightBarrier
from double_motion_actuator import DoubleMotionActuator
from reference_switch import ReferenceSwitch
from single_motion_actuator import SingleMotionActuator
from vacuum_actuator import VacuumActuator


class OvenStation(object):
    """Oven class for oven objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        # Class actuators
        self.oven_carrier = \
            DoubleMotionActuator(self.rpi, 'Oven carrier act', 5, 6)
        self.oven_proc_light = \
            SingleMotionActuator(self.rpi, 'Oven proc light act', 9)
        self.oven_door_opening = \
            VacuumActuator(self.rpi, 'Oven door opening act', 13)
        # Class sensors
        self.inside_oven_switch = \
            ReferenceSwitch(self.rpi, 'inside oven switch', 6)
        self.outside_oven_switch = \
            ReferenceSwitch(self.rpi, 'outside oven switch', 7)
        self.oven_barrier = \
            LightBarrier(self.rpi, 'oven barrier', 9)
        # Class virtual sensors
        self.prod_on_carrier = False
        self.oven_process_completed = False
    
    def get_carrier_position(self) -> str: 
        if self.inside_oven_switch.getState() == True: 
            return 'inside'
        elif self.outside_oven_switch.getState() == True:
            return 'outside'
        else:
            return 'carrier position error'

    def move_carrier_inward(self) -> None:
        self.oven_door_opening.turn_on()
        while (self.inside_oven_switch.getState() == False):
            self.oven_carrier.move_towards_A()
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()

    def move_carrier_outward(self) -> None:
        self.oven_door_opening.turn_on()
        while (self.inside_oven_switch.getState() == False):
            self.oven_carrier.move_towards_B()
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()

    def activate_process_light(self) -> None:
        self.oven_proc_light.turn_on()
    
    def deactivate_process_light(self) -> None:
        self.oven_proc_light.turn_off()