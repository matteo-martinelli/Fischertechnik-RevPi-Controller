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
import time
import json
import logging

from machines.configurations.turntable_carrier_conf import TurntableCarrierConf
from mqtt_conf_listener import MqttConfListener

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs


class TurntableCarrier(object):
    """Turntable Carrier class for turntable objects."""
    def __init__(self, rpi, dept: str, station: str, 
                turntable_clock_act_pin: int, 
                turntable_counterclock_act_pin: int, pusher_act_pin: int, 
                at_vacuum_carrier_sens_pin: int, 
                at_conveyor_carrier_sens_pin: int, at_saw_sens_pin: int, 
                mqtt_publisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')

        # Class descriptive fields
        self._dept = dept
        self._station = station
        self._turntable_pos = 'None'
        self._motor_state = (False, False)
        self._pusher_state = False
        self._prod_on_carrier = False
        self._process_completed = False
        
        self.configuration = TurntableCarrierConf(DefaultStationsConfigs.\
                                                  TURNTABLE_CARRIER_SPEED)

        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        
        self.mqtt_conf_listener = \
            MqttConfListener('multiproc_dept/turntable-carrier/conf', \
                             self.configuration.__class__)
        self.mqtt_conf_listener.open_connection()
        self.read_conf()

        # Class actuators
        # pin 1,2
        self.motor = \
            RevPiDoubleMotionActuator(rpi, 'carrier-motor', 
                                      turntable_clock_act_pin, 
                                      turntable_counterclock_act_pin, 
                                      self.topic, self.mqtt_publisher)
        # pin 14
        self.pusher_activation = \
            RevPiVacuumActuator(rpi, 'pusher-act', pusher_act_pin, 
                                self.topic, self.mqtt_publisher)
        # Class sensors
        # pin 1
        self.at_vacuum_carrier = \
            RevPiReferenceSensor(rpi, 'carrier-at-vacuum', 
                                 at_vacuum_carrier_sens_pin, 
                                 self.topic, self.mqtt_publisher)
        # pin 2
        self.at_conveyor = \
            RevPiReferenceSensor(rpi, 'carrier-at-conveyor', 
                                 at_conveyor_carrier_sens_pin, 
                                 self.topic, self.mqtt_publisher)
        # pin 4
        self.at_saw = \
            RevPiReferenceSensor(rpi, 'carrier-at-saw', at_saw_sens_pin, 
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
    def pusher_state(self) -> bool: 
        return self._pusher_state

    # Sensor
    @property
    def turntable_pos(self) -> str:
        return self._turntable_pos

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

    @motor_state.setter
    def motor_state(self, value: tuple) -> None: 
        if (value != self._motor_state):
            self._motor_state = value
    
    @pusher_state.setter
    def pusher_state(self, value: bool) -> None: 
        if (value != self._pusher_state):
            self._pusher_state = value

    @turntable_pos.setter
    def turntable_pos(self, value: str) -> None: 
        if (value != self._turntable_pos):
            self._turntable_pos = value

    @prod_on_carrier.setter
    def prod_on_carrier(self, value: bool) -> None: 
        if (value != self._prod_on_carrier):
            self._prod_on_carrier = value

    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if (value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    # Class Methods
    def set_prod_on_carrier(self, value: bool) -> None:
        if(value != self._prod_on_carrier):
            self._prod_on_carrier = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    def set_process_completed(self, value: bool) -> None:
        if(value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def push_product(self) -> None: 
        self.activate_pusher()
        self.deactivate_pusher()
    
    def activate_pusher(self) -> None: 
        if(self.pusher_activation.state == False):
            self.pusher_activation.turn_on()
            self.logger.info('turntable pusher activated')
            time.sleep(0.8)
            self.read_pusher_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
            
    def deactivate_pusher(self) -> None: 
        if(self.pusher_activation.state == True):
            self.pusher_activation.turn_off()
            self.logger.info('turntable pusher deactivated')
            time.sleep(0.4)
            self.read_pusher_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    def rotate_towards_saw(self) -> None:
        if(self.at_vacuum_carrier.state == True):
            self.motor.turn_on(self.motor._pin_tuple[0]) # Clockwise
            self.read_motor_state()
            self.read_turntable_pos()
            self.logger.info('turntable activated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
        elif(self.at_conveyor.state == True):
            self.motor.turn_on(self.motor._pin_tuple[1]) # Counter-clockwise
            self.read_motor_state()
            self.read_turntable_pos()
            self.logger.info('turntable activated')
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
        
        # Wait until the turntable reaches the at_saw sensor
        while(self.at_saw.read_state() == False):
            pass

        self.motor.turn_off()
        self.read_motor_state()
        self.read_turntable_pos()
        self.logger.info('turntable deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def rotate_towards_conveyor(self) -> None:
        self.motor.turn_on(self.motor._pin_tuple[0])     # Clockwise
        self.read_motor_state()
        self.read_turntable_pos()
        self.logger.info('turntable activated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        
        # Wait until the turntable reaches the at_conveyor sensor
        while (self.at_conveyor.read_state() == False):
            pass

        self.motor.turn_off()
        self.read_turntable_pos()
        self.read_motor_state()
        self.logger.info('turntable deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def rotate_towards_vacuum_carrier(self) -> None:
        self.motor.turn_on(self.motor._pin_tuple[1])     # Counter-clockwise
        self.read_motor_state()
        self.read_turntable_pos()
        self.logger.info('turntable activated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        
        # Wait until the turntable reaches the at_vacuum_carrier sensor
        while (self.at_vacuum_carrier.read_state() == False):
            pass
        
        self.motor.turn_off()
        self.read_motor_state()
        self.read_turntable_pos()
        self.logger.info('turntable deactivated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def transfer_product_to_saw(self):
        pass

    def transfer_product_to_conveyor(self):
        self.rotate_towards_conveyor()
        self.push_product()
        self.prod_on_carrier = False
        self.rotate_towards_vacuum_carrier()
        self.process_completed = True

    def deactivate_carrier(self) -> None: 
        self.motor.turn_off()
        self.read_motor_state()

        self.pusher_activation.turn_off()
        self.read_pusher_state()
        
        self.set_prod_on_carrier(False)
        self.set_process_completed(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    # Reading underlying sensors/actuators
    # Actuator
    def read_motor_state(self) -> None:
        value = self.motor.read_state()
        if (value != self._motor_state):
            self._motor_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())

    # Actuator
    def read_pusher_state(self) -> None: 
        value = self.pusher_activation.read_state()
        if (value != self._pusher_state):
            self._pusher_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
                
    # Sensor
    def read_turntable_pos(self) -> None:
        at_conveyor = self.at_conveyor.read_state()
        at_vacuum = self.at_vacuum_carrier.read_state()
        at_saw = self.at_saw.read_state()
        
        if (at_vacuum == True
            and self.motor.state[0] == False 
            and self.motor.state[1] == False):
            if (self._turntable_pos != 'vacuum carrier'):
                self._turntable_pos = 'vacuum carrier'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        elif (at_saw == True
            and self.motor.state[0] == False 
            and self.motor.state[1] == False): 
            if (self._turntable_pos != 'saw'):
                self._turntable_pos = 'saw'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json())
        elif (at_conveyor == True
            and self.motor.state[0] == False 
            and self.motor.state[1] == False): 
            if (self._turntable_pos != 'conveyor'):
                self._turntable_pos = 'conveyor'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json())
        elif (self.motor.state[0] == True or 
            self.motor.state[1] == True): 
            if (self._turntable_pos != 'moving'):
                self._turntable_pos = 'moving'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json())
        else: 
            if (self._turntable_pos != 'position error'):
                self._turntable_pos = 'position error'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json())

    def read_all_sensors(self) -> None: 
        self.read_turntable_pos()
        
    def read_all_actuators(self) -> None: 
        self.read_motor_state()
        self.read_pusher_state()

    # MQTT 
    def read_conf(self) -> None: 
        turntable_carrier_speed_conf = self.mqtt_conf_listener.configuration 
        if (turntable_carrier_speed_conf != self.configuration.turntable_carrier_speed 
            and turntable_carrier_speed_conf != None):
            self.configuration = turntable_carrier_speed_conf
            self.logger.info('New configuration received for turntable '
                             'carrier speed {}'\
                             .format(self.configuration\
                                     .turntable_carrier_speed_conf))
        else: 
            self.logger.info('No conf updated, proceeding with the last '
                             'configuration for {}'.format(self.station))

    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'turntable-pos': self._turntable_pos,
            'motor': self.motor._state,
            'pusher-state': self._pusher_state,
            'prod-on-carrier': self._prod_on_carrier,
            'proc-completed': self._process_completed,
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())