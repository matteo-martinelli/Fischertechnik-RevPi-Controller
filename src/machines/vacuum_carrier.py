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

import threading
import revpimodio2
from mqtt.mqtt_publisher import MqttPublisher
from components.revpi_reference_sensor import RevPiReferenceSensor
from components.revpi_double_motion_actuator import RevPiDoubleMotionActuator
from components.revpi_vacuum_actuator import RevPiVacuumActuator
from datetime import datetime
import time
import json
import logging

from mqtt.mqtt_conf_listener import MqttConfListener

from machines.configurations.vacuum_carrier_conf import VacuumCarrierConf
from machines.configurations.default_station_configs \
    import DefaultStationsConfigs

from machines.additional_components.motor_retarder_system import MotorRetarderSystem


class VacuumCarrier(object):
    """Vacuum Carrier class for oven objects."""
    def __init__(self, rpi: revpimodio2.RevPiModIO, dept: str, station: str, 
                 at_turntable_act_pin: int, 
                 at_oven_act_pin: int, grip_act_pin: int, 
                 grip_lower_act_pin: int, at_turntable_sens_pin: int, 
                 at_oven_sens_pin: int, mqtt_publisher: MqttPublisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')

        # Class fields
        self._dept = dept
        self._station = station
        self._motor_state = (False, False)
        self._carrier_position = 'None'
        self._gripper_activation_state = False
        self._gripper_lowering_state = False
        self._prod_on_carrier = False
        self._process_completed = False
        # TODO: make a method that updates the object state and, contextually, publish the change in the mqtt broker

        self.configuration = VacuumCarrierConf(DefaultStationsConfigs.\
                                               VACUUM_CARRIER_SPEED)

        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self._dept + '/' + self._station

        self.mqtt_conf_listener = \
            MqttConfListener('multiproc_dept/vacuum-carrier/conf',
                              self.configuration.to_object)
        self.mqtt_conf_listener.open_connection()
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
        self.motor_retarder = MotorRetarderSystem("vacuum_stop", self.motor)
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
                                                       self.to_json(), True)

    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if (value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # Class Methods
    def activate_gripper(self) -> None: 
        if(self._gripper_activation_state == False):
            self.gripper_activation.turn_on()
            self._gripper_activation_state = True
            self.logger.info('vacuum carrier gripper activated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    def deactivate_gripper(self) -> None: 
        if(self._gripper_activation_state == True):
            self.gripper_activation.turn_off()
            # Fixed time for the pneumatic propagation to take effect
            # Alternative to time.sleep(0.8)
            time_sleep = threading.Thread(name="vacuum_deactivate_gripper", 
                                          target=time.sleep, args=(0.8,)) 
            time_sleep.start()
            time_sleep.join()
            self.read_gripper_activation_state()
            self.logger.info('vacuum carrier gripper deactivated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    def lower_gripper(self) -> None:  
        if(self._gripper_lowering_state == False):
            self.gripper_lowering.turn_on() 
            # Alternative to time.sleep(0.8)
            time_sleep = threading.Thread(name="vacuum_lowering_gripper", 
                                          target=time.sleep, args=(0.8,)) 
            time_sleep.start()
            time_sleep.join()
            self.read_gripper_lowering_state()
            self.logger.info('vacuum carrier gripper lowered')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
    
    def higher_gripper(self) -> None: 
        if(self._gripper_lowering_state == True):
            self.gripper_lowering.turn_off()
            # Alternative to time.sleep(0.4)
            time_sleep = threading.Thread(name="vacuum_highering_gripper", 
                                          target=time.sleep, args=(0.8,)) 
            time_sleep.start()
            time_sleep.join()
            self.read_gripper_lowering_state()
            self.logger.info('vacuum carrier gripper highered')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    def grip_product(self) -> None:
        self.lower_gripper()
        self.activate_gripper()
        self.higher_gripper()
        self.prod_on_carrier = True
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                   self.to_json(), True)

    def release_product(self) -> None:
        self.lower_gripper()
        self.deactivate_gripper()
        self.higher_gripper()
        self.prod_on_carrier = False
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                   self.to_json(), True)

    def move_carrier_towards_oven(self) -> None:
        if(self.at_oven.state == False):
            self.motor.turn_on(self.motor._pin_tuple[0])
            self.logger.info('vacuum carrier activated')
            self._motor_state = (True, False)
            self.read_carrier_position()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

        # Wait until the at_oven sensor turns into True
        # Alternative to:
        #while (self.at_oven.read_state() == False):
        #    pass
        time_sleep = threading.Thread(name="vacuum_carrier_towards_oven_sleep", 
                                      target=self.at_oven_stop_condition, 
                                      args=()) 
        time_sleep.start()
        time_sleep.join()
        
        self.motor.turn_off()
        self.read_carrier_position()
        self.read_motor_state()
        self.logger.info('vacuum carrier deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                   self.to_json(), True)

    def at_oven_stop_condition(self) -> None:
        while (self.at_oven.read_state() == False):
            pass

    def move_carrier_towards_turntable(self) -> None:
        start_time = 0
        if(self.at_turntable.state == False):
            self.motor.turn_on(self.motor._pin_tuple[1])
            start_time = time.time()
            self.read_motor_state()
            self.read_carrier_position()
            self.logger.info('vacuum carrier activated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
        
        # Wait until the at_turntable sensor turns into True
        # Alternative to:
        #if (start_time != 0):
        #    while (time.time() - start_time < 2):
        #        pass
        time_sleep = threading.Thread(name="vacuum_carrier_init_moving", 
                                      target=time.sleep, args=(2,)) 
        time_sleep.start()
        time_sleep.join()
        
        # Carrier speed variation system # Start #
        self.motor_retarder.stop_and_restart_motor(
            self.configuration.vacuum_carrier_speed, 1)  
        # Carrier speed variation system ## End ##
        # Alternative to:
        #while (self.at_turntable.read_state() == False):
        #    pass
        time_sleep = threading.Thread(name="vacuum_carrier_towards_turntable_sleep", 
                                      target=self.at_turntable_stop_condition, 
                                      args=()) 
        time_sleep.start()
        time_sleep.join()
        
        self.motor.turn_off()
        self.read_carrier_position()
        self.read_motor_state()
        self.logger.info('vacuum carrier deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(), 
                                                   True)

    def at_turntable_stop_condition(self) -> None:
        while (self.at_turntable.read_state() == False):
            pass

    def transfer_product_from_oven_to_turntable(self) -> None:
        # TODO: add here a check if the carrier is at the oven; if not, move towards the oven. Then delete the same logic in the multiprocess_manager
        self.grip_product()
        self.move_carrier_towards_turntable()
        self.release_product()
        self.process_completed = True
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                   self.to_json(), True)

    def turn_off_all_actuators(self) -> None: 
        self.motor.turn_off()
        self.read_motor_state()

        self.gripper_activation.turn_off()
        self.read_gripper_activation_state()
        
        self.gripper_lowering.turn_off()
        self.read_gripper_lowering_state()

        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(), 
                                                   True)

    def reset_process_states(self) -> None: 
        self._prod_on_carrier = False
        self._process_completed = False
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(), 
                                                   True)

    def close_connections(self) -> None: 
        self.mqtt_conf_listener.close_connection()

    def reset_carrier(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()        
        
    def deactivate_carrier(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        self.close_connections()
    
    # Reading underlying sensors/actuators
    def read_carrier_position(self) -> None:
        if (self.at_turntable.read_state() == True and
            self.at_oven.read_state() == False and 
            self.motor.state[0] == False and
            self.motor.state[1] == False):
            if(self._carrier_position != 'turntable'):
                self._carrier_position = 'turntable'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(), 
                                                           True)
        elif (self.at_turntable.read_state() == False and
            self.at_oven.read_state() == True and 
            self.motor.state[0] == False and
            self.motor.state[1] == False):
            if(self._carrier_position != 'oven'):
                self._carrier_position = 'oven'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                               self.to_json(), 
                                                               True)
        elif(self.motor.state[0] == True or 
             self.motor.state[1] == True):
            if(self._carrier_position != 'moving'):
                self._carrier_position = 'moving'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json(), 
                                                            True)
        else:
            if(self._carrier_position != 'position error'):
                self._carrier_position = 'position error'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                               self.to_json(), 
                                                               True)

    def read_gripper_lowering_state(self) -> None:
        value = self.gripper_lowering.read_state()
        if (value != self._gripper_lowering_state):
            self._gripper_lowering_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(), 
                                                           True)

    def read_gripper_activation_state(self) -> None: 
        value = self.gripper_activation.read_state()
        if (value != self._gripper_activation_state):
            self._gripper_activation_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(), 
                                                           True)

    def read_motor_state(self) -> None: 
        value = self.motor.read_state()
        if (value != self._motor_state):
            self._motor_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(), 
                                                           True)

    def read_all_sensors(self) -> None:
        self.read_carrier_position()

    def read_all_actuators(self) -> None: 
        self.read_motor_state()
        self.read_gripper_activation_state()
        self.read_gripper_lowering_state()

    # MQTT 
    def read_conf(self) -> None: 
        new_vaccum_carrier_speed_conf = self.mqtt_conf_listener.configuration 
        if (new_vaccum_carrier_speed_conf != None):
            if (new_vaccum_carrier_speed_conf.vacuum_carrier_speed != 
                self.configuration.vacuum_carrier_speed):
                self.logger.info('New configuration received for vacuum '
                                 'carrier speed - old value {}; new value {};'
                                 ' overriding'\
                                 .format(self.configuration\
                                         .vacuum_carrier_speed, 
                                         new_vaccum_carrier_speed_conf\
                                         .vacuum_carrier_speed))
                self.configuration.vacuum_carrier_speed = \
                new_vaccum_carrier_speed_conf.vacuum_carrier_speed
            else: 
                self.logger.info('No conf updated, proceeding with the last '
                            'vacuum carrier speed of {} for {}'\
                            .format(self.configuration.vacuum_carrier_speed, 
                                    self.station))
        else: 
            self.logger.info('No conf updated, proceeding with the last '
                        'vacuum carrier speed of {} for {}'\
                        .format(self.configuration.vacuum_carrier_speed, 
                                self.station))

    def to_dto(self) -> dict:
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
            'carrier-speed': self.configuration.vacuum_carrier_speed,
            'prod-on-carrier': self._prod_on_carrier,
            'proc-completed': self._process_completed,
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self) -> str:
        return json.dumps(self.to_dto())