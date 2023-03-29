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

from components.revpi_light_barrier_sensor import RevPiLightBarrierSensor
from components.revpi_double_motion_actuator import RevPiDoubleMotionActuator
from components.revpi_reference_sensor import RevPiReferenceSensor
from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from components.revpi_vacuum_actuator import RevPiVacuumActuator


class OvenStation(object):
    """Oven class for oven objects."""
    def __init__(self, rpi, carrier_in_act_pin: int, carrier_out_act_pin: int, 
                 proc_light_act_pin: int, vacuum_door_act_pin: int, 
                 in_oven_sens_pin: int, out_oven_sens_pin: int, 
                 light_barrier_sens_pin: int):
        # Class actuators
        self.oven_carrier = \
            RevPiDoubleMotionActuator(rpi, 'Oven carrier act', 
                                      carrier_in_act_pin, 
                                      carrier_out_act_pin)          # 5, 6
        self.oven_proc_light = \
            RevPiSingleMotionActuator(rpi, 'Oven proc light act', 
                                      proc_light_act_pin)           # 9
        self.oven_door_opening = \
            RevPiVacuumActuator(rpi, 'Oven door opening act', 
                                vacuum_door_act_pin)                # 13    
        # Class sensors
        self.inside_oven_switch = \
            RevPiReferenceSensor(rpi, 'inside oven switch', 
                                 in_oven_sens_pin)                  # 6
        self.outside_oven_switch = \
            RevPiReferenceSensor(rpi, 'outside oven switch', 
                                 out_oven_sens_pin)                 # 7
        self.light_barrier = \
            RevPiLightBarrierSensor(rpi, 'oven barrier', 
                                    light_barrier_sens_pin)         # 9
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False


    def get_carrier_position(self) -> str: 
        if (self.inside_oven_switch.get_state() == True): 
            return 'inside'
        if (self.outside_oven_switch.get_state() == True):
            return 'outside'
        if (self.inside_oven_switch.get_state() == False and 
            self.outside_oven_switch.get_state() == False):
            return 'moving'
        if (self.inside_oven_switch.get_state() == True and 
            self.outside_oven_switch.get_state() == True):
            return 'carrier position error'

    def move_carrier_inward(self) -> None:
        self.oven_door_opening.turn_on()
        while (self.inside_oven_switch.get_state() == False):
            self.oven_carrier.turn_on(self.oven_carrier.pin_tuple[0])
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()

    def move_carrier_outward(self) -> None:
        self.oven_door_opening.turn_on()
        while (self.outside_oven_switch.get_state() == False):
            self.oven_carrier.turn_on(self.oven_carrier.pin_tuple[1])
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()
