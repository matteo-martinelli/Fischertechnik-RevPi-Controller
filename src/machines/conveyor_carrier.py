#!/usr/bin/env python

"""
conveyor_carrier.py: ConveyorCarrier class

This class is composed by the following objects: 
    1. single activation motor O_3; 
    2. light barrier sensor I_3;
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from components.revpi_light_barrier_sensor import RevPiLightBarrierSensor
from datetime import datetime
import time
import json
import logging

from machines.configurations.conveyor_carrier_conf import ConveyorCarrierConf
from mqtt.mqtt_conf_listener import MqttConfListener

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs

class ConveyorCarrier(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, rpi, dept: str, station: str, motor_act_pin: int, 
                 barrier_sens_pin: int, mqtt_publisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')
        
        self._dept = dept
        self._station = station
        self._motor_state = False
        self._light_barrier_state = False
        self._prod_on_conveyor = False
        self._process_completed = False
        
        self.configuration = ConveyorCarrierConf(DefaultStationsConfigs
                                                 .CONVEYOR_CARRIER_SPEED)

        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self._dept + '/' + self._station

        self.mqtt_conf_listener = \
            MqttConfListener('multiproc_dept/conveyor-carrier/conf',
                             self.configuration.__class__, 
                             self.configuration.to_object)
        self.mqtt_conf_listener.open_connection()
        self.read_conf()
        
        # Class actuators
        # pin 3
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'motor', motor_act_pin, 
                                      self.topic, mqtt_publisher)
        # Class sensors
        # pin 3
        self.light_barrier = \
            RevPiLightBarrierSensor(rpi, 'light-barrier', 
                                    barrier_sens_pin, self.topic, 
                                    self.mqtt_publisher)
        self.read_all_sensors()
        self.read_all_actuators()

    
    ## Getters
    # Class fields
    @property
    def dept(self) -> str: 
        return self._dept
    
    @property
    def station(self) -> str: 
        return self._station

    # Actuator
    @property
    def motor_state(self) -> bool:
        return self._motor_state

    # Sensor
    @property
    def light_barrier_state(self) -> bool:
        return self._light_barrier_state

    @property
    def prod_on_conveyor(self) -> bool: 
        return self._prod_on_conveyor

    @property
    def process_completed(self) -> bool: 
        return self._process_completed

    ## Setters
    @dept.setter
    def dept(self, value: str) -> None: 
        self._dept = value
    
    @station.setter
    def station(self, value: str) -> None: 
        self._station = value

    @motor_state.setter
    def motor_state(self, value: bool) -> None: 
        self._motor_state = value
    
    @light_barrier_state.setter
    def light_barrier_state(self, value: bool) -> None: 
        self._light_barrier_state = value

    @prod_on_conveyor.setter
    def prod_on_conveyor(self, value: bool) -> None: 
        if(value != self._prod_on_conveyor):
            self._prod_on_conveyor = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if(value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # Class Methods
    # Processes methods
    def move_to_the_exit(self) -> None:
        self.read_conf()
        self.motor.turn_on()
        start_time = time.time()
        self.read_motor_state()
        self.logger.info('conveyor activated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)
        
        # Carrier speed variation system # Start #
        # Wait until the at_turntable sensor turns into True
        if (start_time != 0):
            while (time.time() - start_time < 0.5): 
                pass
        
        self.motor.turn_off()
        carrier_speed = self.configuration.conveyor_carrier_speed
        if (carrier_speed == "Low"):
            time.sleep(5)
        elif (carrier_speed == "Medium"):
            time.sleep(3)
        elif (carrier_speed == "High"):
            time.sleep(2)    
            #pass
        else: 
            self.logger.error('Illegal conveyor speed configuration ' +
                            ' received in moving turntable towards saw;' + 
                            ' expected \"Low\" or \"Medium\" or' +
                            ' \"High\", got %s', carrier_speed)
        self.motor.turn_on() 
        # Carrier speed variation system ## End ##
         
        # Wait until a product reaches the light_barrier sensor
        while (self.light_barrier.read_state() != False):
            pass


        self.motor.turn_off()
        self.read_motor_state()
        self.logger.info('conveyor deactivated')
        self.process_completed = True
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def turn_off_all_actuators(self) -> None: 
        self.motor.turn_off()
        self.read_motor_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def reset_process_states(self) -> None: 
        self._prod_on_conveyor = False
        self._process_completed = False
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def closing_connections(self) -> None: 
        pass

    def reset_carrier(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        
    def deactivate_carrier(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        #self.mqtt_conf_listener.close_connection                               -> actually not present

    # Reading underlying sensors/actuators
    def read_motor_state(self) -> None: # QUESTA E' UNA LETTURA
        value = self.motor.read_state()
        if (value != self._motor_state):
            self._motor_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic,
                                                       self.to_json(), True)

    def read_light_barrier_state(self) -> None: # QUESTA E' UNA LETTURA 
        value = self.light_barrier.read_state()
        if (value != self._light_barrier_state):
            self._light_barrier_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
    
    # Read all sensors and actuators
    def read_all_sensors(self) -> None: 
        self.read_light_barrier_state()
    
    def read_all_actuators(self) -> None: 
        self.read_motor_state()

    # MQTT 
    def read_conf(self) -> None: 
        new_conveyor_carrier_speed_conf = self.mqtt_conf_listener.configuration 
        if (new_conveyor_carrier_speed_conf != None):
            if (new_conveyor_carrier_speed_conf.conveyor_carrier_speed != 
                self.configuration.conveyor_carrier_speed):
                self.logger.info('New configuration received for conveyor '
                                'carrier speed - old value {}; new value {}; '
                                'overriding'\
                                .format(self.configuration\
                                        .conveyor_carrier_speed, 
                                        new_conveyor_carrier_speed_conf\
                                        .conveyor_carrier_speed))
                self.configuration.conveyor_carrier_speed = \
                    new_conveyor_carrier_speed_conf.conveyor_carrier_speed
            else: 
                self.logger.info('No conf updated, proceeding with the last '
                                 'carrier speed of {} for {}'\
                                 .format(self.configuration.\
                                         conveyor_carrier_speed, 
                                         self.station))
        else: 
                self.logger.info('No conf updated, proceeding with the last '
                                 'carrier speed of {} for {}'\
                                 .format(self.configuration.\
                                         conveyor_carrier_speed, 
                                         self.station))

    def to_dto(self):
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'conveyor_motor': self._motor_state,
            'light-barrier': self._light_barrier_state,
            'prod-on-carrier': self._prod_on_conveyor,
            'proc-completed': self._process_completed,
            
            'timestamp': timestamp,
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
