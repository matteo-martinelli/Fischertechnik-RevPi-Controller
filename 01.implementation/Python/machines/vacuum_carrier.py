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

from components.revpi_reference_sensor import RevPiReferenceSensor
from components.revpi_double_motion_actuator import RevPiDoubleMotionActuator
from components.revpi_vacuum_actuator import RevPiVacuumActuator
from datetime import datetime
import time
import json


class VacuumCarrier(object):
    """Vacuum Carrier class for oven objects."""
    def __init__(self, rpi, dept: str, station: str, at_turntable_act_pin: int,
                 at_oven_act_pin: int, grip_act_pin: int, 
                 grip_lower_act_pin: int, at_turntable_sens_pin: int, 
                 at_oven_sens_pin: int, mqtt_publisher):
        # Class descriptive fields
        self.dept = dept
        self.station = station
        self.carrier_pos = 'None'
        self.gripper_lowering_state = False
        self.gripper_state = False
        # Class actuators
        self.motor = \
            RevPiDoubleMotionActuator(rpi, 'Vacuum carrier motor', 
                                      at_turntable_act_pin, 
                                      at_oven_act_pin)                  # 7, 8
        self.gripper_activation = \
            RevPiVacuumActuator(rpi, 'vacuum gripper', grip_act_pin)    # 11
        self.gripper_lowering = \
            RevPiVacuumActuator(rpi, 'vacuum gripper lowering', 
                                grip_lower_act_pin)                     # 12
        # Class sensors
        self.at_turntable = \
            RevPiReferenceSensor(rpi, 'towards turntable ref switch', 
                                 at_turntable_sens_pin)                 # 5
        self.at_oven = \
            RevPiReferenceSensor(rpi, 'towards oven ref switch', 
                                 at_oven_sens_pin)                      # 8
        # Initializing class fields
        self.carrier_pos = self.get_carrier_position()
        self.gripper_lowering_state = self.gripper_activation.get_state()
        self.gripper_state = self.gripper_lowering.get_state()
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station


    # Setters
    def set_prod_on_carrier(self, value: bool) -> None: 
        self.prod_on_carrier = value
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def set_process_completed(self, value: bool) -> None: 
        self.process_completed = value
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    # Getters
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station

    def get_prod_on_carrier(self) -> bool: 
        return self.prod_on_carrier
    
    def get_process_completed(self) -> bool: 
        return self.process_completed
        
    def get_gripper_lowering_state(self) -> bool: 
        return self.gripper_lowering.get_state()

    def get_gripper_activation_state(self) -> bool: 
        return self.gripper_activation.get_state()

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

    # Class Methods
    def activate_gripper(self) -> None: 
        self.gripper_activation.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_gripper(self) -> None: 
        self.gripper_activation.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def lower_gripper(self) -> None: 
        self.gripper_lowering.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def higher_gripper(self) -> None: 
        self.gripper_lowering.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def move_carrier_towards_oven(self) -> None:
        counter = 0

        while (self.at_oven.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[0])
            if (counter == 0): 
                counter += 1
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        self.motor.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def move_carrier_towards_turntable(self) -> None:
        counter = 0

        while (self.at_turntable.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[1])
            if (counter == 0): 
                counter += 1
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        self.motor.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.gripper_activation.turn_off()
        self.gripper_lowering.turn_off()
        self.set_prod_on_carrier(False)
        self.set_process_completed(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")
        
        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'carrier-pos': self.carrier_pos,
            'grip-low-state': self.gripper_lowering_state, 
            'grip-state': self.gripper_state,
            'motor': self.motor.get_state(),
            'prod-on-carrier': self.get_prod_on_carrier(),
            'proc-completed': self.get_process_completed(),
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())