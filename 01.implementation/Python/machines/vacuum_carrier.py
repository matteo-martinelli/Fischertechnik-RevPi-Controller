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
        self._dept = dept
        self._station = station
        self._motor_state = (False, False)
        self._carrier_position = 'None'
        self._gripper_activation_state = False
        self._gripper_lowering_state = False
        self._prod_on_carrier = False
        self._process_completed = False

        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self._dept + '/' + self._station
        
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
        self.read_all_sensors()
        self.read_all_actuators()


    ## Getters ##
    @property
    def dept(self) -> str: 
        return self._dept
    
    @property
    def station(self) -> str: 
        return self._station
    
    # Actuator
    @property
    def motor_state(self) -> tuple: 
        return self._motor_state
    
    # Actuator
    @property
    def gripper_lowering_state(self) -> bool: 
        return self._gripper_lowering_state
        
    # Actuator
    @property
    def gripper_activation_state(self) -> bool: 
        return self._gripper_activation_state
        
    # Sensor
    @property
    def carrier_position(self) -> str: 
        return self._carrier_position

    @property
    def prod_on_carrier(self) -> bool: 
        return self._prod_on_carrier
    
    @property
    def process_completed(self) -> bool: 
        return self._process_completed

    ## Setters ##
    @dept.setter
    def dept(self, value: str) -> None: 
        self._dept = value
    
    @station.setter
    def station(self, value: str) -> None: 
        self._station = value
    
    # Actuator
    @motor_state.setter
    def motor_state(self, value: tuple) -> None: 
        if (value != self._motor_state):
            self._motor_state = value

    # Actuator
    @gripper_lowering_state.setter
    def gripper_lowering_state(self, value: bool) -> None: 
        if (value != self._gripper_lowering_state):
            self._gripper_lowering_state = value
    
    # Actuator
    @gripper_activation_state.setter
    def gripper_activation_state(self, value: bool) -> None: 
        if (value != self._gripper_activation_state):
            self._gripper_activation_state = value
    
    # Sensor
    @carrier_position.setter
    def carrier_position(self, value: str) -> None: 
        if (value != self._carrier_position):
            self._carrier_position = value

    @prod_on_carrier.setter
    def prod_on_carrier(self, value: bool) -> None: 
        if (value != self._prod_on_carrier):
            self._prod_on_carrier = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if (value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    # Class Methods
    def activate_gripper(self) -> None: 
        if(self._gripper_activation_state == False):
            self.gripper_activation.turn_on()
            self._gripper_activation_state = True
            print('vacuum carrier gripper activated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def deactivate_gripper(self) -> None: 
        if(self._gripper_activation_state == True):
            self.gripper_activation.turn_off()
            # Fixed time for the pneumatic propagation to take effect
            time.sleep(0.8)
            self.read_gripper_activation_state()
            print('vacuum carrier gripper deactivated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def lower_gripper(self) -> None:  
        if(self._gripper_lowering_state == False):
            self.gripper_lowering.turn_on() 
            time.sleep(0.8)
            self.read_gripper_lowering_state()
            print('vacuum carrier gripper lowered')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    def higher_gripper(self) -> None: 
        if(self._gripper_lowering_state == True):
            self.gripper_lowering.turn_off()
            time.sleep(0.4)
            self.read_gripper_lowering_state()
            print('vacuum carrier gripper highered')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def move_carrier_towards_oven(self) -> None:
        if(self.at_oven.state == False):
            self.motor.turn_on(self.motor._pin_tuple[0])
            print('vacuum carrier activated')
            self._motor_state = (True, False)
            self.read_carrier_position()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

        # Wait until the at_oven sensor turns into True
        while (self.at_oven.read_state() == False):
            pass
        
        self.motor.turn_off()
        self.read_carrier_position()
        self.read_motor_state()
        print('vacuum carrier deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                   self.to_json())

    def move_carrier_towards_turntable(self) -> None:
        if(self.at_turntable.state == False):
            self.motor.turn_on(self.motor._pin_tuple[1])
            self.read_motor_state()
            self.read_carrier_position()
            print('vacuum carrier activated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

        # Wait until the at_turntable sensor turns into True
        while (self.at_turntable.read_state() == False):
            pass

        self.motor.turn_off()
        self.read_carrier_position()
        self.read_motor_state()
        print('vacuum carrier deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.read_motor_state()

        self.gripper_activation.turn_off()
        self.read_gripper_activation_state()
        
        self.gripper_lowering.turn_off()
        self.read_gripper_lowering_state()

        self._prod_on_carrier = False
        self._process_completed = False
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    # Reading underlying sensors/actuators
    def read_carrier_position(self) -> None:
        if (self.at_turntable.read_state() == True and
            self.at_oven.read_state() == False and 
            self.motor.state[0] == False and
            self.motor.state[1] == False):
            if(self._carrier_position != 'turntable'):
                self._carrier_position = 'turntable'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        elif (self.at_turntable.read_state() == False and
            self.at_oven.read_state() == True and 
            self.motor.state[0] == False and
            self.motor.state[1] == False):
            if(self._carrier_position != 'oven'):
                self._carrier_position = 'oven'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                               self.to_json())
        elif(self.motor.state[0] == True or 
             self.motor.state[1] == True):
            if(self._carrier_position != 'moving'):
                self._carrier_position = 'moving'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json())
        else:
            if(self._carrier_position != 'position error'):
                self._carrier_position = 'position error'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                               self.to_json())

    def read_gripper_lowering_state(self) -> None:
        value = self.gripper_lowering.read_state()
        if (value != self._gripper_lowering_state):
            self._gripper_lowering_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())

    def read_gripper_activation_state(self) -> None: 
        value = self.gripper_activation.read_state()
        if (value != self._gripper_activation_state):
            self._gripper_activation_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())

    def read_motor_state(self) -> None: 
        value = self.motor.read_state()
        if (value != self._motor_state):
            self._motor_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())

    def read_all_sensors(self) -> None:
        self.read_carrier_position()

    def read_all_actuators(self) -> None: 
        self.read_motor_state()
        self.read_gripper_activation_state()
        self.read_gripper_lowering_state()

    # MQTT 
    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")
        
        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'carrier-pos': self._carrier_position,
            'grip-low-state': self._gripper_lowering_state, 
            'grip-state': self._gripper_activation_state,
            'motor': self._motor_state,
            'prod-on-carrier': self._prod_on_carrier,
            'proc-completed': self._process_completed,
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())