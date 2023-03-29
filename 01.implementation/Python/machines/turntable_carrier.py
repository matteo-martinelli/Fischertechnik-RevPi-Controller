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

from components.revpi_reference_sensor import RevPiReferenceSensor
from components.revpi_double_motion_actuator import RevPiDoubleMotionActuator
from components.revpi_vacuum_actuator import RevPiVacuumActuator


class TurntableCarrier(object):
    """Turntable Carrier class for turntable objects."""
    def __init__(self, rpi, turntable_clock_act_pin: int, 
                 turntable_counterclock_act_pin: int, pusher_act_pin: int, 
                 at_vacuum_carrier_sens_pin: int, at_conveyor_carrier_sens_pin: int, 
                 at_saw_sens_pin: int):
        # Class actuators
        self.motor = \
            RevPiDoubleMotionActuator(rpi, 'Vacuum carrier motor', 
                                      turntable_clock_act_pin, 
                                      turntable_counterclock_act_pin)   # 1, 2
        self.pusher_activation = \
            RevPiVacuumActuator(rpi, 'vacuum gripper', pusher_act_pin)  # 14
        # Class sensors
        self.at_vacuum_carrier = \
            RevPiReferenceSensor(rpi, 'towards turntable ref switch', 
                                 at_vacuum_carrier_sens_pin)            # 1
        self.at_conveyor = \
            RevPiReferenceSensor(rpi, 'towards oven ref switch', 
                                 at_conveyor_carrier_sens_pin)          # 2
        self.at_saw = \
            RevPiReferenceSensor(rpi, 'towards oven ref switch', 
                                 at_saw_sens_pin)                       # 4
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False


    def rotate_towards_saw(self) -> None:
        while (self.at_saw.get_state() == False):
            if (self.at_vacuum_carrier.get_state() == True):
                self.motor.turn_on(self.motor.pin_tuple[0]) # Clockwise
            elif (self.at_conveyor.get_state() == True):
                self.motor.turn_on(self.motor.pin_tuple[1]) # Counter-clockwise
        self.motor.turn_off()

    def rotate_towards_conveyor(self) -> None:
        while (self.at_conveyor.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[0]) # Clockwise
        self.motor.turn_off()

    def rotate_towards_vacuum_carrier(self) -> None:
        while (self.at_vacuum_carrier.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[1]) # Counterclockwise
        self.motor.turn_off()

    def get_carrier_position(self) -> str: 
        if (self.at_vacuum_carrier.get_state() == True):
            return 'vacuum carrier'
        elif (self.at_saw.get_state() == True): 
            return 'saw'
        elif (self.at_conveyor.get_state() == True): 
            return 'conveyor'
        elif (self.at_vacuum_carrier.get_state() == False and 
              self.at_saw.get_state() == False and 
              self.at_conveyor.get_state() == False): 
            return 'moving'
        else: 
            return 'position error'
