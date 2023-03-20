#!/usr/bin/env python

"""
oven.py: Oven class

This class is composed by the following objects: 
    1. light barrier sensor I_9; 
    2. double actuated product carrier O_5, O_6; 
    3. vacuum actuated oven door O_13;
    4. inward reference switch I_6;
    5. outward reference switch I_7;
    6. process light O_9. 
"""

from components.light_barrier import LightBarrier
from components.double_motion_actuator import DoubleMotionActuator
from components.reference_switch import ReferenceSwitch
from components.single_motion_actuator import SingleMotionActuator
from components.vacuum_actuator import VacuumActuator


class OvenStation(object):
    """Oven class for oven objects."""
    def __init__(self, rpi):
        # Class actuators
        self.oven_carrier = \
            DoubleMotionActuator(rpi, 'Oven carrier act', 5, 6)
        self.oven_proc_light = \
            SingleMotionActuator(rpi, 'Oven proc light act', 9)
        self.oven_door_opening = \
            VacuumActuator(rpi, 'Oven door opening act', 13)
        # Class sensors
        self.inside_oven_switch = \
            ReferenceSwitch(rpi, 'inside oven switch', 6)
        self.outside_oven_switch = \
            ReferenceSwitch(rpi, 'outside oven switch', 7)
        self.light_barrier = \
            LightBarrier(rpi, 'oven barrier', 9)
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False
    
    def get_light_barrier_state(self) -> bool: 
        return self.light_barrier.getState()

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
        while (self.outside_oven_switch.getState() == False):
            self.oven_carrier.move_towards_B()
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()

    def activate_process_light(self) -> None:
        self.oven_proc_light.turn_on()
    
    def deactivate_process_light(self) -> None:
        self.oven_proc_light.turn_off()