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
from datetime import datetime
import json


class TurntableCarrier(object):
    """Turntable Carrier class for turntable objects."""
    def __init__(self, rpi, dept: str, station: str, 
                turntable_clock_act_pin: int, 
                turntable_counterclock_act_pin: int, pusher_act_pin: int, 
                at_vacuum_carrier_sens_pin: int, 
                at_conveyor_carrier_sens_pin: int, at_saw_sens_pin: int, 
                mqtt_publisher):
        # Class descriptive fields
        self.dept = dept
        self.station = station
        self.turntable_pos = self.get_carrier_position()
        self.pusher_state = self.pusher_activation.get_state()
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
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = 'put/some/topic'   # TODO: eventually change it


    # Setters
    def set_prod_on_carrier(self, value: bool) -> None: 
        self.prod_on_carrier = value

    def set_process_completed(self, value: bool) -> None: 
        self.process_completed = value
    
    # Getters
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station
    
    def get_pusher_state(self) -> bool: 
        return self.pusher_state

    def get_prod_on_conveyor(self) -> bool: 
        return self.prod_on_carrier

    def get_process_completed(self) -> bool: 
        return self.process_completed

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

    # Class Methods
    def activate_pusher(self) -> None: 
        self.pusher_activation.turn_on()
    
    def deactivate_pusher(self) -> None: 
        self.pusher_activation.turn_off()
    
    def rotate_towards_saw(self) -> None:
        while (self.at_saw.get_state() == False):
            if (self.at_vacuum_carrier.get_state() == True):
                self.motor.turn_on(self.motor.pin_tuple[0]) # Clockwise
            elif (self.at_conveyor.get_state() == True):
                self.motor.turn_on(self.motor.pin_tuple[1]) # Counter-clockwise
        self.motor.turn_off()

    def rotate_towards_conveyor(self) -> None:
        while (self.at_conveyor.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[0])     # Clockwise
        self.motor.turn_off()

    def rotate_towards_vacuum_carrier(self) -> None:
        while (self.at_vacuum_carrier.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[1])     # Counter-clockwise
        self.motor.turn_off()

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.pusher_activation.turn_off()
        self.set_prod_on_carrier(False)
        self.set_process_completed(False)

    # MQTT 
    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'turntable-pos': self.turntable_pos,
            'pusher-state': self.pusher_state,
            'prod-on-carrier': self.get_prod_on_conveyor(),
            'proc-completed': self.get_process_completed(),
            
            'timestamp': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())