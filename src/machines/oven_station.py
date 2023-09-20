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

from machines.configurations.oven_station_conf import OvenStationConf
from mqtt.mqtt_conf_listener import MqttConfListener

import threading
from datetime import datetime 
import time
import json
import logging

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs   #TODO: eventually change it
from machines.oven_station_temperature_control import calc_state 
from machines.oven_station_temperature_control import update_temperature 


class OvenStation(object):
    """Oven class for oven objects."""
    def __init__(self, rpi, dept: str, station: str, 
                 carrier_in_act_pin: int, carrier_out_act_pin: int, 
                 proc_light_act_pin: int, vacuum_door_act_pin: int, 
                 in_oven_sens_pin, out_oven_sens_pin: int, 
                 light_barrier_sens_pin: int, mqtt_publisher):
        
        self.logger = logging.getLogger('multiproc_dept_logger')     

        # Class fields
        self._dept = dept
        self._station = station
        self._carrier_pos = 'None'
        self._door_pos = False
        self._proc_light_state = False
        self._prod_on_carrier = False
        self._process_completed = False
        self._light_barrier_state = False
        
        # numbers from real product sheet
        # TODO: add them to your initialisiation
        # //https://www.gpline.com.tw/productdetail_en.php?id=427
        self.oven_state ='warming'                      # Oven state
        self.stop_event = threading.Event()             # Cool down stop flag 
        self.cooling_oven_process = None                # Cooling process field
        self.room_temperature = 24.0                    # Physical
        self.temperature_inside = self.room_temperature # Physical
        self.set_temperature = 60.0                     # Conf - 300 from prod
        self.insulation = None                          # Physical
        self.fluctuation = 5.0                          # Physical - 3.0 from prod
        self.max_temperature = 100.0                    # Conf - 400 from prod
        self.min_set_temperature = 100.0                # Conf

        self.configuration = OvenStationConf(DefaultStationsConfigs.\
                                             OVEN_PROCESSING_TIME)
        
        # MQTT
        self.mqtt_publisher = mqtt_publisher
        self.topic = self._dept + '/' + self._station

        self.mqtt_conf_listener = \
            MqttConfListener('multiproc_dept/oven-station/conf', 
                             self.configuration.__class__, self.configuration.to_object)
        self.mqtt_conf_listener.open_connection()
        self.read_conf()

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
        self.read_all_sensors()
        self.read_all_actuators()


    ## Getters
    @property
    def dept(self) -> str: 
        return self._dept
    
    @property
    def station(self) -> str: 
        return self._station
    
    # Sensor
    @property
    def light_barrier_state(self) -> bool: 
        return self._light_barrier_state
    
    # Sensor
    @property
    def carrier_pos(self) -> str:
        return self._carrier_pos
    
    # Actuator
    @property
    def proc_light_state(self) -> bool: 
        return self._proc_light_state
        
    # Actuator
    @property
    def door_pos(self) -> bool:
        return self._door_pos
    
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

    @light_barrier_state.setter
    def light_barrier_state(self, value: bool) -> None: 
        if (value != self._light_barrier_state):
            self._light_barrier_state = value
    
    @carrier_pos.setter
    def carrier_pos(self, value: str) -> None: 
        if (value != self._carrier_pos):
            self._carrier_pos = value

    @door_pos.setter
    def door_pos(self, value: bool) -> None: 
        if (value != self._door_pos):
            self._door_pos = value

    @proc_light_state.setter
    def proc_light_state(self, value: bool) -> None: 
        if (value != self._proc_light_state):
            self._proc_light_state = value

    @prod_on_carrier.setter
    def prod_on_carrier(self, value: bool) -> None: 
        if (value != self._prod_on_carrier):
            self._prod_on_carrier = value
    
    @process_completed.setter
    def process_completed(self, value: bool) -> None: 
        if (value != self._process_completed):
            self._process_completed = value
    
    # Class Methods
    def move_carrier_inward(self) -> None:
        self.oven_door_opening.turn_on()
        self.read_door_pos()
        self.logger.info('oven door opened')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

        self.oven_carrier.turn_on(self.oven_carrier._pin_tuple[0])
        self.read_carrier_position()
        self.read_light_barrier_state()
        self.logger.info('oven carrier activated')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

        # Wait until the oven carrier reaches the outward oven switch
        while (self.inside_oven_switch.read_state() == False):
            self.read_carrier_position()
            self.read_light_barrier_state()
        
        self.oven_carrier.turn_off()
        self.read_carrier_position()
        self.logger.info('oven carrier deactivated')
        self.read_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)
        
        self.oven_door_opening.turn_off()
        self.read_door_pos()
        self.logger.info('oven door closed')
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def move_carrier_outward(self) -> None:
        self.oven_door_opening.turn_on()
        self.read_door_pos()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

        self.oven_carrier.turn_on(self.oven_carrier._pin_tuple[1])
        self.read_carrier_position()
        self.read_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

        # Wait until the oven carrier reaches the outward oven switch
        while (self.outside_oven_switch.read_state() == False):
            self.read_light_barrier_state()
            
        self.oven_carrier.turn_off()
        self.read_carrier_position()
        self.read_light_barrier_state()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)
        self.oven_door_opening.turn_off()
        self.read_door_pos()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def activate_proc_light(self) -> None:
        if (self.oven_proc_light.state == False):
            self.oven_proc_light.turn_on()
            self.read_proc_light_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
    
    def deactivate_proc_light(self) -> None:
        if (self.oven_proc_light.state == True):
            self.oven_proc_light.turn_off()
            self.read_proc_light_state()
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
    
    #def oven_process_start(self, proc_time, target_temperature = 300.0) -> None:
    def oven_process_start(self, target_temperature = 200.0) -> None:
        self.read_conf()

        # for each product, start producing ...
        self.move_carrier_inward()

        #self.activate_proc_light()
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(), 
                                                   True)
        
        # heating up
        self.heat_oven_up(target_temperature)

        # process the piece
        self.oven_keep_temp(self.configuration.oven_processing_time)
        
        # done processing, preparing the cooling down thread
        self.cooling_oven_process = threading.Thread(name="oven_cooling_process", # TODO: add the process termination at ctrl + C in the right method
                                                 target=self.cool_oven_down, 
                                                 args=(self.room_temperature,))
        # cooling down                          # When not deamon, the main thread cannot exit - Not necessary here
        self.cooling_oven_process.start()
                
        self.move_carrier_outward()
        self.set_process_completed(True)

    def check_oven_if_cooling(self):
        if (self.cooling_oven_process is not None):
            logging.debug("Oven cooling process is running. Stopping it")
            self.stop_event.set()
            self.cooling_oven_process.join()
            self.cooling_oven_process = None
            logging.debug("Oven cooling process stopped")
        else: 
            logging.debug("Oven is not cooling down, heating it up")

    def heat_oven_up(self, target_temp):
        self.check_oven_if_cooling()
        
        self.set_temperature = target_temp
        self.logger.info('Oven activated')
        
        # publish data
        self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                    self.to_json(), True)

        while self.temperature_inside + self.fluctuation < self.set_temperature:
            self.activate_proc_light()
            self.temperature_inside, self.oven_state = \
                update_temperature(self.room_temperature, 
                                    self.temperature_inside, 
                                    self.set_temperature, 
                                    self.fluctuation, 
                                    self.min_set_temperature, 
                                    self.max_temperature, 1, 'unknown')
            self.logger.info('Heating up, oven state {}, temp {}°C'.\
                             format(self.oven_state, self.temperature_inside))
            time.sleep(1)
            # publish data
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                    self.to_json(), True)

        self.logger.info('Target temp reached, oven state {}, temp {}°C'.\
                         format(self.oven_state, self.temperature_inside))
        
    def oven_keep_temp(self, processing_time):
        for i in range(processing_time):
            self.temperature_inside, self.oven_state = \
                update_temperature(self.room_temperature, 
                                    self.temperature_inside, 
                                    self.set_temperature, 
                                    self.fluctuation, 
                                    self.min_set_temperature, 
                                    self.max_temperature, 1, 'unknown')
            
            if self.oven_state == "heating" or self.oven_state == "warming":
                self.activate_proc_light()
            if self.oven_state == "cooling":
                self.deactivate_proc_light()

            self.logger.info('Processing the product: oven state {},' 
                             ' oven temp {}°C'.\
                             format(self.oven_state, self.temperature_inside))
            
            time.sleep(1)
            #time.sleep(self.configuration.oven_processing_time) # TODO: eventually change into time.sleep(configuration.proc_time)
            
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                    self.to_json(), True)
        
        # end for, done producing ...
        self.logger.info('Oven processing complete')
        
        # deactivating processing light
        self.deactivate_proc_light()

    def cool_oven_down(self, target_temperature: float):
        # publish data
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(), 
                                                   True)
        
        # updating the temperature
        while self.temperature_inside - self.fluctuation > target_temperature:
            self.temperature_inside, self.oven_state = \
                update_temperature(self.room_temperature, 
                                    self.temperature_inside, 
                                    target_temperature, 
                                    self.fluctuation, 
                                    self.min_set_temperature, 
                                    self.max_temperature, 1, 'unknown')
            
            self.logger.info('cooling down, oven state {}, temp {}°C'.\
                             format(self.oven_state, self.temperature_inside))
            
            time.sleep(1)
            
            # publish data
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)
            
            # thread stop flag check
            if self.stop_event.is_set(): 
                self.stop_event.clear()
                logging.debug("Cooling phase interrupted."\
                              " Last temperature: {}"\
                                .format(self.temperature_inside))
                break

    def turn_off_all_actuators(self) -> None: 
        self.oven_carrier.turn_off()
        self.read_carrier_position()

        self.oven_proc_light.turn_off()
        self.read_proc_light_state()
        
        self.oven_door_opening.turn_off()
        self.read_door_pos()

        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def reset_process_states(self) -> None: 
        self.set_process_completed(False)
        self.set_prod_on_carrier(False)
        self.mqtt_publisher.publish_telemetry_data(self.topic, self.to_json(),
                                                   True)

    def close_connections(self) -> None: 
        self.mqtt_conf_listener.close_connection()

    def reset_station(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        
    def deactivate_station(self) -> None: 
        self.turn_off_all_actuators()
        self.reset_process_states()
        self.close_connections()
        self.stop_event.set()

    def set_prod_on_carrier(self, value: bool) -> None:
        if(value != self._prod_on_carrier):
            self._prod_on_carrier = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    def set_process_completed(self, value: bool) -> None:
        if(value != self._process_completed):
            self._process_completed = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # Reading underlying sensors/actuators
    # Sensor
    def read_light_barrier_state(self) -> None:  # LETTURA
        light_barrier_read = self.light_barrier.read_state()
        process_complete = self.process_completed
        if (light_barrier_read == False):
            if (process_complete == False):
                self.set_prod_on_carrier(True)
        
        if (light_barrier_read == True):
            if (process_complete == True):
                self.set_prod_on_carrier(False)
        
        if (light_barrier_read != self._light_barrier_state):
            self._light_barrier_state = light_barrier_read
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                       self.to_json(), True)

    # Sensor
    def read_carrier_position(self) -> None:     # LETTURA
        if (self.inside_oven_switch.read_state() == True
            and self.oven_carrier.state[0] == False
            and self.oven_carrier.state[1] == False): 
            if (self._carrier_pos != 'inside'):
                self._carrier_pos = 'inside'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                            self.to_json(),
                                                            True)
        elif (self.outside_oven_switch.read_state() == True
            and self.oven_carrier.state[0] == False
            and self.oven_carrier.state[1] == False):
            if (self._carrier_pos != 'outside'):
                self._carrier_pos = 'outside'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(),
                                                            True)
        elif (self.oven_carrier.state[0] == True 
            or self.oven_carrier.state[1] == True):
            if (self._carrier_pos != 'moving'):
                self._carrier_pos = 'moving'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(),
                                                            True)
        elif (self.inside_oven_switch.read_state() == True and 
            self.outside_oven_switch.read_state() == True):
            if (self._carrier_pos != 'carrier position error'):
                self._carrier_pos = 'carrier position error'
                self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(),
                                                           True)

    # Actuator     
    def read_door_pos(self) -> None:
        value = self.oven_door_opening.read_state()
        if (value != self._door_pos):
            self._door_pos = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(), 
                                                           True)

    # Actuator
    def read_proc_light_state(self) -> None:
        value = self.oven_proc_light.read_state()
        if (self._proc_light_state != value):
            self._proc_light_state = value
            self.mqtt_publisher.publish_telemetry_data(self.topic, 
                                                           self.to_json(), 
                                                           True)

    def read_all_sensors(self) -> None: 
        self.read_light_barrier_state()
        self.read_carrier_position()

    def read_all_actuators(self) -> None: 
        self.read_door_pos()
        self.read_proc_light_state()

    # MQTT 
    def read_conf(self) -> None: # TODO: why it has been changed?
    #    new_oven_proc_time_conf = self.mqtt_conf_listener.configuration
    #    if (new_oven_proc_time_conf != None):
    #        if (new_oven_proc_time_conf.oven_processing_time != 
    #            self.configuration.oven_processing_time):
    #            self.logger.info('New configuration received for oven station '
    #                         'process time - old value {}; new value {}; '
    #                         'overriding'\
    #                         .format(self.configuration.oven_processing_time, 
    #                                new_oven_proc_time_conf\
    #                                .oven_processing_time))
    #            self.configuration.oven_processing_time = \
    #            new_oven_proc_time_conf.oven_processing_time
    #        else: 
    #            self.logger.info('No conf updated, proceeding with the last '
    #                             'oven_proc_time of {} for {}'\
    #                             .format(self.configuration.\
    #                                     oven_processing_time, 
    #                                     self.station))
    #    else: 
    #        self.logger.info('No conf updated, proceeding with the last '
    #                         'oven_proc_time of {} for {}'\
    #                         .format(self.configuration.oven_processing_time, 
    #                                 self.station))
        oven_proc_time_conf = self.mqtt_conf_listener.configuration 
        if (oven_proc_time_conf != self.configuration._oven_processing_time 
            and oven_proc_time_conf != None):
            self.configuration = oven_proc_time_conf
            print('New configuration received for oven station process time ',\
                  self.configuration.oven_processing_time)
        
    def to_dto(self):   # Data Transfer Objet
        timestamp = time.time()
        current_moment = \
            datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'dept': self._dept,
            'station': self._station,
            'type': self.__class__.__name__,
            'layer': 'machine',
            'oven-carrier': self._carrier_pos,
            'oven-door': self._door_pos,
            'proc-light': self._proc_light_state,
            'oven-temp': self.temperature_inside,
            'oven-heating-state': self.oven_state,
            'light-barrier': self._light_barrier_state,
            'prod-on-carrier': self._prod_on_carrier,
            'proc-completed': self._process_completed,
            
            'timestamp': int(timestamp),
            'current-time': current_moment
        }

        return dto_dict

    def to_json(self):
        return json.dumps(self.to_dto())
