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
        # Class descriptive fields
        self.dept = dept
        self.station = station
        #self.state = False     # Helpful to track the 'idle' or 'working'state of a machine?
        #self.carrier_pos = self.get_carrier_position()  
        #self.door_pos = False
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self.dept + '/' + self.station
        # Class actuators
        self.oven_carrier = \
            RevPiDoubleMotionActuator(rpi, 'Oven carrier act', 
                                      carrier_in_act_pin, 
                                      carrier_out_act_pin)          # 5, 6
        self.oven_door_opening = \
            RevPiVacuumActuator(rpi, 'Oven door opening act', 
                                vacuum_door_act_pin)                # 13    
        self.oven_proc_light = \
            RevPiSingleMotionActuator(rpi, 'Oven proc light act', 
                                      proc_light_act_pin, self.topic, mqtt_publisher)           # 9
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
        # Initializing class fields 
        #self.carrier_pos = self.get_carrier_position()  
        #self.door_pos = self.get_door_pos()
        # Class virtual sensors
        self.prod_on_carrier = False
        self.process_completed = False


    # Setters
    #def set_state(self, value: bool) ->None: 
    #    self.state = value

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
    
    #def get_state(self) -> bool: 
    #    return self.state

    def get_prod_on_carrier(self) -> bool: 
        return self.prod_on_carrier

    def get_process_completed(self) -> bool: 
        return self.process_completed
    
    def get_light_barrier_state(self) -> bool: 
        return self.light_barrier.get_state()
        # MQTT publish

    def get_proc_light_state(self) -> bool: 
        return self.oven_proc_light.get_state()

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
    
    def get_door_pos(self) -> bool: 
        return self.oven_door_opening.get_state()
        
    # Class Methods
    def move_carrier_inward(self) -> None:
        counter = 0
        self.oven_door_opening.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

        while (self.inside_oven_switch.get_state() == False):
            self.oven_carrier.turn_on(self.oven_carrier.pin_tuple[0])
            if (counter == 0):
                counter += 1
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def move_carrier_outward(self) -> None:
        counter = 0
        self.oven_door_opening.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

        while (self.outside_oven_switch.get_state() == False):
            self.oven_carrier.turn_on(self.oven_carrier.pin_tuple[1])
            if(counter == 0): 
                counter += 1 
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json())
        self.oven_carrier.turn_off()
        self.oven_door_opening.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def activate_proc_light(self) -> None:
        self.oven_proc_light.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    def deactivate_proc_light(self) -> None:
        self.oven_proc_light.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
    
    # TODO: test this function if works
    def oven_process_start(self, proc_time: int) -> None:
        self.oven_proc_light.turn_on()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())
        time.sleep(proc_time)
        self.oven_proc_light.turn_off()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    def deactivate_station(self) -> None: 
        self.oven_carrier.turn_off()
        self.oven_proc_light.turn_off()
        self.oven_door_opening.turn_off()
        self.set_process_completed(False)
        self.set_prod_on_carrier(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json())

    # MQTT 
    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self.dept,
            'station': self.station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            #'carrier-pos': self.carrier_pos,
            #'door-pos': self.door_pos, 
            'oven-carrier': self.get_carrier_position(),
            'oven-door': self.get_door_pos(),
            #'proc-light': self.oven_proc_light.get_state() # TODO: adapt, since flashes
            'light-barrier': self.get_light_barrier_state(),
            'prod-on-carrier': self.get_prod_on_carrier(),
            'proc-completed': self.get_process_completed(),
            
            'timestamp': current_moment
        }
        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())