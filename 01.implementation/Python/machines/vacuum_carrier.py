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
        # Class fields
        self.dept = dept
        self.station = station
        self.motor_state = False
        self.carrier_pos = 'None'
        self.gripper_activation_state = False
        self.gripper_lowering_state = False
        self.prod_on_carrier = False
        self.process_completed = False

        #self.last_carrier_pos = 'None'  # TODO: implement for getters and MQTT
        #self.last_gripper_activation_state = False
        #self.last_gripper_lowering_state = False
        #self.last_prod_on_carrier = False
        #self.last_process_completed = False
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        # Class actuators
        # pin 7,8
        self.motor = \
            RevPiDoubleMotionActuator(rpi, 'motor', 
                                      at_turntable_act_pin, at_oven_act_pin, 
                                      self.topic, self.mqtt_publisher)
        # pin 11
        self.gripper_activation = \
            RevPiVacuumActuator(rpi, 'gripper', grip_act_pin, 
                                self.topic, self.mqtt_publisher)
        # pin 12
        self.gripper_lowering = \
            RevPiVacuumActuator(rpi, 'gripper-lowering', grip_lower_act_pin, 
                                self.topic, self.mqtt_publisher)
        # Class sensors
        # pin 5
        self.at_turntable = \
            RevPiReferenceSensor(rpi, 'carrier-at-turntable', 
                                 at_turntable_sens_pin, 
                                 self.topic, self.mqtt_publisher)
        # pin 8
        self.at_oven = \
            RevPiReferenceSensor(rpi, 'carrier-at-oven', at_oven_sens_pin, 
                                 self.topic, self.mqtt_publisher)
        
        # Initializing class fields
        self.set_carrier_position()
        

    ## Setters ##
    # Actuator
    def set_motor_state(self) -> None: 
        value = self.motor.state
        if (value != self.motor_state):
            self.motor_state = value

    # Actuator
    def set_gripper_activation_state(self) -> None: 
        value = self.gripper_activation.get_state()
        if (value != self.gripper_activation):
            self.gripper_activation_state = value
    
    # Actuator
    def set_gripper_lowering_state(self) -> None:
        value = self.gripper_lowering.get_state()
        if (value != self.gripper_lowering_state):
            self.gripper_lowering_state = value
    
    # Sensor
    def set_carrier_position(self) -> None:
        if (self.at_turntable.get_state() == True and
            self.at_oven.get_state() == False and 
            self.motor.get_state()[0] == False and
            self.motor.get_state()[1] == False):
            if(self.carrier_pos != 'turntable'):
                self.carrier_pos = 'turntable'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        elif (self.at_turntable.get_state() == False and
            self.at_oven.get_state() == True and 
            self.motor.get_state()[0] == False and
            self.motor.get_state()[1] == False):
            if(self.carrier_pos != 'oven'):
                self.carrier_pos = 'oven'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                               self.to_json())
        elif(self.motor.get_state()[0] == True or 
             self.motor.get_state()[1] == True):
            if(self.carrier_pos != 'moving'):
                self.carrier_pos = 'moving'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json())
        else:
            if(self.carrier_pos != 'position error'):
                self.carrier_pos = 'position error'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                               self.to_json())

    def set_prod_on_carrier(self, value: bool) -> None: 
        if(value != self.get_prod_on_carrier()):
            self.prod_on_carrier = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def set_process_completed(self, value: bool) -> None: 
        if (value != self.get_process_completed()):
            self.process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    ## Getters ##
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station
    
    # Actuator
    def get_motor_state(self) -> bool: 
        return self.motor_state
    
    # Actuator
    def get_gripper_lowering_state(self) -> bool: 
        #if (self.gripper_lowering_state != self.last_gripper_lowering_state):
        #    self.last_gripper_lowering_state = self.gripper_lowering_state
        #    self.mqtt_publisher.publish_telemetry_data(self.topic, 
        #                                               self.to_json())
        return self.gripper_lowering_state
        #return self.gripper_lowering.get_state()

    # Actuator
    def get_gripper_activation_state(self) -> bool: 
        #if (self.gripper_activation_state != self.last_gripper_activation_state):
        #    self.last_gripper_activation_state = self.gripper_activation_state
        #    self.mqtt_publisher.publish_telemetry_data(self.topic, 
        #                                               self.to_json())
        return self.gripper_activation_state
        #return self.gripper_activation.get_state()

    # Sensor
    def get_carrier_position(self) -> str: 
        #if (self.carrier_pos != self.last_carrier_pos):
        #    self.last_carrier_pos = self.carrier_pos
        #    self.mqtt_publisher.publish_telemetry_data(self.topic, 
        #                                               self.to_json())
        return self.carrier_pos

    def get_prod_on_carrier(self) -> bool: 
        return self.prod_on_carrier
    
    def get_process_completed(self) -> bool: 
        return self.process_completed

    # Class Methods
    def activate_gripper(self) -> None: 
        if(self.gripper_activation.get_state() == False):
            self.gripper_activation.turn_on()
            self.set_gripper_activation_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def deactivate_gripper(self) -> None: 
        if(self.gripper_activation.get_state() == True):
            self.gripper_activation.turn_off()
            self.set_gripper_activation_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def lower_gripper(self) -> None: 
        if(self.gripper_lowering.get_state() == False):
            self.gripper_lowering.turn_on()
            self.set_gripper_lowering_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def higher_gripper(self) -> None: 
        if(self.gripper_lowering.get_state() == True):
            self.gripper_lowering.turn_off()
            self.set_gripper_lowering_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def move_carrier_towards_oven(self) -> None:
        if(self.at_oven.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[0])
            self.set_motor_state()
            self.set_carrier_position()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

        # Wait until the at_oven sensor turns into True
        while (self.at_oven.get_state() == False):
            pass
        
        self.motor.turn_off()
        self.set_carrier_position()
        self.set_motor_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                   self.to_json())

    def move_carrier_towards_turntable(self) -> None:
        if(self.at_turntable.get_state() == False):
            self.motor.turn_on(self.motor.pin_tuple[1])
            self.set_motor_state()
            self.set_carrier_position()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

        # Wait until the at_turntable sensor turns into True
        while (self.at_turntable.get_state() == False):
            pass

        self.motor.turn_off()
        self.set_carrier_position()
        self.set_motor_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.set_motor_state()

        self.gripper_activation.turn_off()
        self.set_gripper_activation_state()
        
        self.gripper_lowering.turn_off()
        self.set_gripper_lowering_state()

        self.set_prod_on_carrier(False)
        self.set_process_completed(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")
        
        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'carrier-pos': self.get_carrier_position(),
            'grip-low-state': self.get_gripper_lowering_state(), 
            'grip-state': self.get_gripper_activation_state(),
            'motor': self.get_motor_state(),
            'prod-on-carrier': self.get_prod_on_carrier(),
            'proc-completed': self.get_process_completed(),
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())