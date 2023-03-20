#!/usr/bin/env python

"""
vacuum_carrier.py: VacuumCarrier class

This class is composed by the following objects: 
    1. towards oven reference switch I_8; 
    2. towards turntable reference switch I_5;
    3. double actuated carrier O_7 O_8; 
    4. vacuum actuated gripper raiser and lowerer O_12;
    5. vacuum gripper O_11; 
"""

from components.reference_switch import ReferenceSwitch
from components.double_motion_actuator import DoubleMotionActuator
from components.vacuum_actuator import VacuumActuator


class VacuumCarrier(object):
    """Vacuum Carrier class for oven objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        #self.rpi = rpi
        # Class actuators
        self.motor = \
            DoubleMotionActuator(rpi, 'Vacuum carrier motor', 7, 8)
        self.gripper_activation = \
            VacuumActuator(rpi, 'vacuum gripper', 11)
        self.gripper_lowering = \
            VacuumActuator(rpi, 'vacuum gripper lowering', 12)
        # Class sensors
        self.at_turntable = \
            ReferenceSwitch(rpi, 'towards turntable ref switch', 5)
        self.at_oven = \
            ReferenceSwitch(rpi, 'towards oven ref switch', 8)
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False


    def get_carrier_position(self) -> str: 
        if (self.at_turntable.getState() == True):
            return 'turntable'
        elif (self.at_oven.getState() == True):
            return 'oven'
        else:
            return 'position error'

    def move_carrier_towards_oven(self) -> None:
        while (self.at_oven.getState() == False):
            self.motor.move_towards_A()
        self.motor.turn_off()

    def move_carrier_towards_turntable(self) -> None:
        while (self.at_turntable.getState() == False):
            self.motor.move_towards_B()
        self.motor.turn_off()

    def stop_carrier(self) -> None:
        self.motor.turn_off()
    
    def lower_vac_gripper(self) -> None:
        self.gripper_lowering.turn_on()
    
    def raise_vac_gripper(self) -> None:
        self.gripper_lowering.turn_off()

    def get_vac_position(self) -> str: 
        if (self.gripper_lowering.getState() == True):
            return 'low'
        else: 
            return 'high'

    def grip_object(self) -> None: 
        self.gripper_activation.turn_on()
    
    def release_object(self) -> None: 
        self.gripper_activation.turn_off()
    
    def get_gripper_state(self) -> str: 
        if (self.gripper_activation.getState() == True):
            return 'activated'
        else: 
            return 'deactivated'
