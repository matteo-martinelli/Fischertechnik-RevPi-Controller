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

from components.revpi_reference_switch import RevPiReferenceSwitch
from components.revpi_double_motion_actuator import RevPiDoubleMotionActuator
from components.revpi_vacuum_actuator import RevPiVacuumActuator


class VacuumCarrier(object):
    """Vacuum Carrier class for oven objects."""
    def __init__(self, rpi):
        # Class actuators
        self.motor = \
            RevPiDoubleMotionActuator(rpi, 'Vacuum carrier motor', 7, 8)
        self.gripper_activation = \
            RevPiVacuumActuator(rpi, 'vacuum gripper', 11)
        self.gripper_lowering = \
            RevPiVacuumActuator(rpi, 'vacuum gripper lowering', 12)
        # Class sensors
        self.at_turntable = \
            RevPiReferenceSwitch(rpi, 'towards turntable ref switch', 5)
        self.at_oven = \
            RevPiReferenceSwitch(rpi, 'towards oven ref switch', 8)
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False

    # TODO: add carrier pos field?
    def get_carrier_position(self) -> str: 
        if (self.at_turntable.get_state() == True and
            self.at_oven.get_state() == False):
            return 'turntable'
        elif (self.at_turntable.get_state() == False and
            self.at_oven.get_state() == True):
            return 'oven'
        elif(self.at_turntable.get_state() == False and
            self.at_oven.get_state() == False):
            return 'moving'
        else:
            return 'position error'

    def move_carrier_towards_oven(self) -> None:
        while (self.at_oven.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[0])
        self.motor.turn_off()

    def move_carrier_towards_turntable(self) -> None:
        while (self.at_turntable.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[1])
        self.motor.turn_off()
        
"""
    def stop_carrier(self) -> None:
        self.motor.turn_off()
    
    def lower_vac_gripper(self) -> None:
        self.gripper_lowering.turn_on()
    
    def raise_vac_gripper(self) -> None:
        self.gripper_lowering.turn_off()

    def get_vac_position(self) -> str: 
        if (self.gripper_lowering.get_state() == True):
            return 'low'
        else: 
            return 'high'

    def grip_object(self) -> None: 
        self.gripper_activation.turn_on()
    
    def release_object(self) -> None: 
        self.gripper_activation.turn_off()
    
    def get_gripper_state(self) -> str: 
        if (self.gripper_activation.get_state() == True):
            return 'activated'
        else: 
            return 'deactivated'
"""