#!/usr/bin/env python

"""
turntable_carrier.py: TurnTableCarrier class

This class is composed by the following objects: 
    1. towards vacuum carrier reference switch I_1; 
    2. towards conveyor reference switch I_2;
    3. towards saw reference switch I_4;
    4. double actuated motor O_1 O_2;
    5. vacuum actuated pusher O_14;
"""

from components.reference_switch import ReferenceSwitch
from components.double_motion_actuator import DoubleMotionActuator
from components.vacuum_actuator import VacuumActuator


class TurntableCarrier(object):
    """Turntable Carrier class for turntable objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        # Class actuators
        self.motor = \
            DoubleMotionActuator(self.rpi, 'Vacuum carrier motor', 1, 2)
        self.pusher_activation = \
            VacuumActuator(self.rpi, 'vacuum gripper', 14)
        # Class sensors
        self.at_vacuum_carrier = \
            ReferenceSwitch(self.rpi, 'towards turntable ref switch', 1)
        self.at_conveyor = \
            ReferenceSwitch(self.rpi, 'towards oven ref switch', 2)
        self.at_saw = \
            ReferenceSwitch(self.rpi, 'towards oven ref switch', 4)
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False


    def rotate_towards_saw(self) -> None:
        while (self.at_saw.getState() == False):
            if (self.at_vacuum_carrier.getState() == True):
                self.motor.move_towards_A() # Clockwise
            elif (self.at_conveyor.getState() == True):
                self.motor.move_towards_B() # Counter-clockwise
        self.motor.turn_off()

    def rotate_towards_conveyor(self) -> None:
        while (self.at_conveyor.getState() == False):
            self.motor.move_towards_A() # Clockwise
        self.motor.turn_off()

    def rotate_towards_vacuum_carrier(self) -> None:
        while (self.at_vacuum_carrier.getState() == False):
            self.motor.move_towards_B() # Clockwise
        self.motor.turn_off()

    def get_carrier_position(self) -> str: 
        if (self.at_vacuum_carrier.getState() == True):
            return 'vacuum carrier'
        elif (self.at_saw.getState() == True): 
            return 'saw'
        elif (self.at_conveyor.getState() == True): 
            return 'conveyor'
        else: 
            return 'position error'

    def stop_carrier(self) -> None:
        self.motor.turn_off()
    
    def activate_pusher(self) -> None: 
        self.pusher_activation.turn_on()

    def deactivate_pusher(self) -> None: 
        self.pusher_activation.turn_off()
    
    def get_pusher_state(self) -> str: 
        if (self.pusher_activation.getState() == True):
            return 'activated'
        else: 
            return 'deactivated'
