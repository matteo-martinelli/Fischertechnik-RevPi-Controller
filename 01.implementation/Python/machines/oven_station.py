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

from datetime import datetime 
import time
import json


class OvenStation(object):
    """Oven class for oven objects."""
    def __init__(self, rpi, dept: str, station: str, 
                 carrier_in_act_pin: int, carrier_out_act_pin: int, 
                 proc_light_act_pin: int, vacuum_door_act_pin: int, 
                 in_oven_sens_pin: int, out_oven_sens_pin: int, 
                 light_barrier_sens_pin: int, mqtt_publisher):
        # Class fields
        self.dept = dept
        self.station = station
        self.carrier_pos = 'None'
        self.door_pos = False
        self.proc_light_state = False
        self.prod_on_carrier = False
        self.process_completed = False
        self.light_barrier_state = False
        
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        
        # Class actuators
        # pin 5, 6
        self.oven_carrier = \
            RevPiDoubleMotionActuator(rpi, 'carrier-motor', 
                                      carrier_in_act_pin, 
                                      carrier_out_act_pin, self.topic, 
                                      self.mqtt_publisher)
        # pin 13
        self.oven_door_opening = \
            RevPiVacuumActuator(rpi, 'door-motor', 
                                vacuum_door_act_pin, 
                                self.topic, self.mqtt_publisher)    
        # pin 9
        self.oven_proc_light = \
            RevPiSingleMotionActuator(rpi, 'proc-light', 
                                      proc_light_act_pin, self.topic, 
                                      mqtt_publisher)
        # Class sensors
        # pin 6
        self.inside_oven_switch = \
            RevPiReferenceSensor(rpi, 'carrier-inside', 
                                 in_oven_sens_pin, 
                                 self.topic, self.mqtt_publisher)
        # pin 7
        self.outside_oven_switch = \
            RevPiReferenceSensor(rpi, 'carrier-outside', 
                                 out_oven_sens_pin, 
                                 self.topic, self.mqtt_publisher)
        # pin 9
        self.light_barrier = \
            RevPiLightBarrierSensor(rpi, 'oven-light-barrier', 
                                    light_barrier_sens_pin, 
                                    self.topic, self.mqtt_publisher)
        # Initialising class fields
        self.read_sensors()
        self.read_actuators()
        self.set_prod_on_carrier(False)
        self.set_process_completed(False)
        
    # Read all sensors and actuators
    def read_sensors(self) -> None: 
        self.set_light_barrier_state()
        self.set_carrier_position()

    def read_actuators(self) -> None: 
        self.set_door_pos()
        self.set_proc_light_state()

    ## Setters ##
    # Sensor
    def set_light_barrier_state(self) -> None:
        value = self.light_barrier.get_state()
        if (value != self.light_barrier_state):
            self.light_barrier_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    # Sensor
    def set_carrier_position(self) -> None:
        if (self.inside_oven_switch.get_state() == True
            and self.oven_carrier.get_state()[0] == False
            and self.oven_carrier.get_state()[1] == False): 
            if (self.carrier_pos != 'inside'):
                self.carrier_pos = 'inside'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        elif (self.outside_oven_switch.get_state() == True
            and self.oven_carrier.get_state()[0] == False
            and self.oven_carrier.get_state()[1] == False):
            if (self.carrier_pos != 'outside'):
                self.carrier_pos = 'outside'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        elif (self.oven_carrier.get_state()[0] == True 
            or self.oven_carrier.get_state()[1] == True):
            if (self.carrier_pos != 'moving'):
                self.carrier_pos = 'moving'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        elif (self.inside_oven_switch.get_state() == True and 
            self.outside_oven_switch.get_state() == True):
            if (self.carrier_pos != 'carrier position error'):
                self.carrier_pos = 'carrier position error'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())

    # Actuator     
    def set_door_pos(self) -> None:
        if (self.oven_door_opening.get_state() == True):
            self.door_pos = True
        else: 
            self.door_pos = False

    # Actuator
    def set_proc_light_state(self) -> None:
        value = self.oven_proc_light.get_state()
        if (self.proc_light_state != value):
            self.proc_light_state = value
    
    def set_prod_on_carrier(self, value: bool) -> None: 
        if(value != self.get_prod_on_carrier()):
            self.prod_on_carrier = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())

    def set_process_completed(self, value: bool) -> None: 
        if(value != self.get_process_completed()):
            self.process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    ## Getters ##
    def get_dept(self) -> str: 
        return self.dept
    
    def get_station(self) -> str: 
        return self.station
    
    # Sensor
    def get_light_barrier_state(self) -> bool: 
        return self.light_barrier_state
    
    # Sensor
    def get_carrier_position(self) -> str:
        return self.carrier_pos
    
    # Actuator
    def get_proc_light_state(self) -> bool: 
        return self.proc_light_state
        
    # Actuator
    def get_door_pos(self) -> bool:
        return self.door_pos
        
    def get_prod_on_carrier(self) -> bool: 
        return self.prod_on_carrier

    def get_process_completed(self) -> bool: 
        return self.process_completed
    
    # Class Methods
    def move_carrier_inward(self) -> None:
        self.oven_door_opening.turn_on()
        self.set_door_pos()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

        self.oven_carrier.turn_on(self.oven_carrier.pin_tuple[0])
        self.set_carrier_position()
        self.set_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

        # Wait until the oven carrier reaches the outward oven switch
        while (self.inside_oven_switch.get_state() == False):
            self.set_carrier_position()
            self.set_light_barrier_state()
        
        self.oven_carrier.turn_off()
        self.set_carrier_position()
        self.set_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        
        self.oven_door_opening.turn_off()
        self.set_door_pos()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def move_carrier_outward(self) -> None:
        self.oven_door_opening.turn_on()
        self.set_door_pos()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

        self.oven_carrier.turn_on(self.oven_carrier.pin_tuple[1])
        self.set_carrier_position()
        self.set_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

        # Wait until the oven carrier reaches the outward oven switch
        while (self.outside_oven_switch.get_state() == False):
            self.set_light_barrier_state()
            self.get_light_barrier_state()

        self.oven_carrier.turn_off()
        self.set_carrier_position()
        self.set_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        self.oven_door_opening.turn_off()
        self.set_door_pos()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def activate_proc_light(self) -> None:
        if (self.oven_proc_light.get_state() == False):
            self.oven_proc_light.turn_on()
            self.set_proc_light_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    def deactivate_proc_light(self) -> None:
        if (self.oven_proc_light.get_state() == True):
            self.oven_proc_light.turn_off()
            self.set_proc_light_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json())
    
    # TODO: test this function if works
    def oven_process_start(self, proc_time: int) -> None:
        self.oven_proc_light.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        time.sleep(proc_time)
        self.oven_proc_light.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_station(self) -> None: 
        self.oven_carrier.turn_off()
        self.set_carrier_position()

        self.oven_proc_light.turn_off()
        self.set_proc_light_state()
        
        self.oven_door_opening.turn_off()
        self.set_door_pos()

        self.set_process_completed(False)
        self.set_prod_on_carrier(False)
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
            'oven-carrier': self.get_carrier_position(),
            'oven-door': self.get_door_pos(),
            'proc-light': self.get_proc_light_state(),
            'light-barrier': self.get_light_barrier_state(),
            'prod-on-carrier': self.get_prod_on_carrier(),
            'proc-completed': self.get_process_completed(),
            
            'timestamp': int(timestamp),
            'current-time': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())