#!/usr/bin/env python

"""
multiprocess_manager.py: MultiprocessManager class

This class is aimed at controlling the whole Fischertechnik loop process.
It contains the RevPi mainloop, and every class used should be attached to this 
file.

The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


# TODO: add sensors pubblication only if the last value changed
# TODO: on DT, infer workign status as follows: if proc_complete=false and prod_on_carrier=true -> working else waiting else completed
import revpimodio2
import time
import logging

from mqtt_publisher import MqttPublisher
from mqtt_conf_listener import MqttConfListener

from machines.compressor_service import CompressorService
from machines.oven_station import OvenStation
from machines.vacuum_carrier import VacuumCarrier
from machines.turntable_carrier import TurntableCarrier
from machines.saw_station import SawStation
from machines.conveyor_carrier import ConveyorCarrier
from conf.multiproc_dept_conf import MultiProcDeptConf

from machines.configurations.default_station_configs \
    import DefaultStationsConfigs


class MultiprocessManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""

    def __init__(self, dept_name):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup)
        # Logger
        logging.basicConfig(format='[%(asctime)s] - %(message)s', 
                            datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
        self.logger = logging.getLogger('multiproc_dept_logger')

        # Process config
        self.process_conf = \
            MultiProcDeptConf(
            pieces_to_produce=DefaultStationsConfigs.PIECES_TO_PRODUCE, 
            compressor_behaviour=DefaultStationsConfigs.COMPRESSOR_BEHAVIOUR,
            oven_processing_time=DefaultStationsConfigs.OVEN_PROCESSING_TIME,      # Time in seconds
            saw_processing_time=DefaultStationsConfigs.SAW_PROCESSING_TIME,        # Time in seconds
            vacuum_carrier_speed=DefaultStationsConfigs.VACUUM_CARRIER_SPEED,      # TBD
            turntable_carrier_speed=DefaultStationsConfigs.TURNTABLE_CARRIER_SPEED # TBD
            )

        # Instantiating the MQTT publisher
        self.mqtt_publisher = MqttPublisher('user:dept_manager/multiproc_dept')
        self.mqtt_conf_listener = MqttConfListener('multiproc_dept/conf',\
                                                   self.process_conf.__class__)
        self.dept_name = dept_name  # Dept mqtt root topic
        
        # My aggregated objects
        self.oven_station = \
            OvenStation(self.rpi, self.dept_name, 'oven-station', 5, 6, 9, 13,
                         6, 7, 9, self.mqtt_publisher)
        self.vacuum_gripper_carrier = \
            VacuumCarrier(self.rpi, self.dept_name, 'vacuum-carrier', 7, 8, 11,
                           12, 5, 8, self.mqtt_publisher)
        self.turntable_carrier = \
            TurntableCarrier(self.rpi, self.dept_name, 'turntable-carrier', 1, 
                             2, 14, 1, 2, 4, self.mqtt_publisher)
        self.saw_station = \
            SawStation(self.rpi, self.dept_name, 'saw-station', 4, 
                       self.mqtt_publisher)
        self.conveyor_carrier = \
            ConveyorCarrier(self.rpi, self.dept_name, 'conveyor-carrier',
                            3, 3, self.mqtt_publisher)

        self.compressor_service = \
            CompressorService(self.rpi, self.dept_name, 'compressor-service', 
                              10, self.mqtt_publisher)

        # Process fileds
        self.pieces_counter = 0
        self.process_completed = False
        self.to_reset = False

    def set_received_configuration(self, conf):
        self.logger.info('a configuration have been saved')
        self.process_conf.pieces_to_produce = conf.pieces_to_produce
        self.process_conf.compressor_behaviour = conf.compressor_behaviour
        self.process_conf.oven_processing_time = conf.oven_processing_time
        self.process_conf.saw_processing_time = conf.saw_processing_time
        self.process_conf.vacuum_carrier_speed = conf.vacuum_carrier_speed
        self.process_conf.turntable_carrier_speed = \
            conf.turntable_carrier_speed
    
    def read_all_sensors(self):
        self.oven_station.read_all_sensors()            # Oven station
        self.vacuum_gripper_carrier.read_all_sensors()  # Vacuum carrier  
        self.turntable_carrier.read_all_sensors()       # Turntable carrier
        # no senors!                                    # Saw station
        self.conveyor_carrier.read_all_sensors()        # Conveyor station
    
    def cleanup(self):
        """Cleanup function to leave the RevPi in a defined state."""
        self.logger.info('Cleaning the system state')

        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False                                     # type: ignore

        # Closing the MQTT connection
        self.mqtt_publisher.close_connection()
        self.mqtt_conf_listener.close_connection()

        # Turning off all the system actuators and resetting stations states
        self.compressor_service.deactivate_service()
        self.oven_station.deactivate_station()
        self.vacuum_gripper_carrier.deactivate_carrier()
        self.turntable_carrier.deactivate_carrier()
        self.saw_station.deactivate_station()
        self.conveyor_carrier.deactivate_carrier()

        # Cleaning the object support states
        self.reset_station_states_and_stop()
    
    def reset_station_states_and_stop(self):
        self.reset_station_states_and_restart
        self.compressor_service.deactivate_service()
    
    def reset_station_states_and_restart(self):
        # Turning off all the system actuators and resetting stations states
        # TODO: change all those methods into restarts; into the deactivate methods add the mqtt conf listener close connection
        self.oven_station.deactivate_station()
        self.vacuum_gripper_carrier.deactivate_carrier()
        self.turntable_carrier.deactivate_carrier()
        self.saw_station.deactivate_station()
        self.conveyor_carrier.deactivate_carrier()

    def start(self):        
        """Start event system and own cyclic loop."""
        self.logger.info('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        # Sets the Rpi a1 light: switch on / off green part of LED A1
        self.rpi.core.a1green.value = not self.rpi.core.a1green.value           # type: ignore


        # Connecting to the MQTT broker 
        # With the publisher
        self.mqtt_publisher.open_connection() 
        # With the configuration listener
        self.mqtt_conf_listener.open_connection()
        time.sleep(0.5)
        if(self.mqtt_conf_listener.configuration != None):
            self.set_received_configuration(
                self.mqtt_conf_listener.configuration)
            self.logger.info('New conf saved found for {}, '
                             'uploaded '.format(self.dept_name))
        else: 
            self.logger.info('No conf saved found, proceeding the standard '    
                             'conf for {}'.format(self.dept_name))
        
        # Activating the process services - i.e. the compressor_service
        self.compressor_service.activate_service()

        self.logger.info('Waiting for the first piece to process')

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 2 things, continuously: 
        #   1. Sets the Rpi a1 light
        #   2. Follows the process description
        # The cycle is set in ... .exitsignal.wait(0.05) every 0.05s
        while (self.rpi.exitsignal.wait(0.05) == False):
            # TODO: simplify the process loop
            # TODO: move "process complete check" and various positioning checks inside classes -> To do so you have to perform one check of all sensors at the end of each process -> though to do as is necessary to associte "near machines classes"
            # First things first: reading all the sensors states
            self.read_all_sensors()
            # Follows the process description #################################
            # If there is the product on the oven_station carrier, move the 
            # vacuum carrier towards the oven_station
            if (self.oven_station.process_completed == False and 
                self.oven_station.prod_on_carrier == True):
                if (self.vacuum_gripper_carrier.carrier_position != 'oven'):
                    self.vacuum_gripper_carrier.move_carrier_towards_oven()
                    
            # If the oven_station process is not completed and the vacuum 
            # carrier grip is at the oven_station and the product is on the 
            # oven_station carrier, start the oven process 
            if (self.oven_station.process_completed == False and
                self.oven_station.prod_on_carrier == True and 
                self.vacuum_gripper_carrier.carrier_position == 'oven'):
                    self.oven_station.oven_process_start(self.process_conf.\
                                                         oven_processing_time)

            # Check that the turntable is rotated towards the vacuum_carrier, 
            # then transfer the product with the vacuum_carrier
            if (self.oven_station.carrier_pos == 'outside' and 
                self.oven_station.process_completed == True and
                self.oven_station.prod_on_carrier == True and
                self.vacuum_gripper_carrier.carrier_position == 'oven'):
            
                # Rotate the turntable towards the vacuum carrier
                self.turntable_carrier.rotate_towards_vacuum_carrier()

                # Grip the product
                self.oven_station.prod_on_carrier = False
                self.vacuum_gripper_carrier.\
                    transfer_product_from_oven_to_turntable()
                self.turntable_carrier.prod_on_carrier = True
                    
            # Turn the turntable towards the saw
            if (self.turntable_carrier.prod_on_carrier == True and
                self.turntable_carrier.process_completed == False):
                # Activate the turntable until it reaches the saw
                if (self.turntable_carrier.turntable_pos != 'saw' and
                    self.saw_station.process_completed == False):
                    self.turntable_carrier.rotate_towards_saw()
                    self.saw_station.prod_under_saw = True

                # Activate the saw for the designed processing time
                if (self.turntable_carrier.turntable_pos == 'saw' and 
                    self.saw_station.process_completed == False):
                    self.saw_station.processing(self.process_conf.\
                                                saw_processing_time)
            
                # Activate the turntable until it reaches the conveyor                
                if (self.saw_station.process_completed == True and
                    self.turntable_carrier.turntable_pos != 'conveyor'):                    
                    self.saw_station.prod_under_saw = False
                    self.turntable_carrier.transfer_product_to_conveyor()
                    self.conveyor_carrier.prod_on_conveyor = True
            
            # Activate the conveyor
            if (self.conveyor_carrier.prod_on_conveyor == True
                and self.conveyor_carrier.process_completed == False):
                # Move towards exit
                if (self.conveyor_carrier.light_barrier_state == True):
                    self.conveyor_carrier.move_to_the_exit()

            ###################################################################
            # If there is the product in front of the light sensor
            if(self.conveyor_carrier.light_barrier_state == False 
               and self.conveyor_carrier.process_completed == True 
               and self.turntable_carrier.process_completed == True 
               and self.saw_station.process_completed == True 
               and self.vacuum_gripper_carrier.process_completed == True 
               and self.oven_station.process_completed == True
               and self.process_completed == False):
                # Add 1 to the piece counter
                self.pieces_counter += 1
                # Setting the process as completed
                self.process_completed = True
                self.to_reset = True
                # Print the process completion message
                self.logger.info('piece completed')
                pieces_left = \
                    self.process_conf.pieces_to_produce - self.pieces_counter
                self.logger.info('{} pieces left to be produced'\
                             .format(pieces_left))

            ###################################################################
            # If the product is in moved from the conveyor light barrier, reset
            # everything, and set the dept as ready to restart
            if(self.conveyor_carrier.light_barrier_state == True 
               and self.process_completed == True
               and self.to_reset == True):
                if(self.pieces_counter == self.process_conf.pieces_to_produce):
                    # Print the process completion message
                    self.logger.info('production completed,'
                                     'terminating the program cycle')
                    self.reset_station_states_and_stop()
                    break
                else:
                    self.logger.info('Accepting another piece')
                    # Reset the system
                    self.conveyor_carrier.prod_on_conveyor = False
                    self.reset_station_states_and_restart()
                    self.to_reset = False
                    self.process_completed = False
                    ('Waiting')

if __name__ == "__main__":
    # Instantiating the controlling class
    root = MultiprocessManager('multiproc_dept')
    # Launch the start function of the RevPi event control system
    root.start()
