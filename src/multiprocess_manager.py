#!/usr/bin/env python

"""
multiprocess_manager.py: MultiprocessManager class

This class is aimed at controlling the whole Fischertechnik loop process.
It contains the RevPi mainloop, and every class used should be attached to this 
file.

The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
import time
import logging

from mqtt.mqtt_publisher import MqttPublisher
from mqtt.mqtt_conf_listener import MqttConfListener

from machines.compressor_service import CompressorService
from machines.oven_station import OvenStation
from machines.vacuum_carrier import VacuumCarrier
from machines.turntable_carrier import TurntableCarrier
from machines.saw_station import SawStation
from machines.conveyor_carrier import ConveyorCarrier

from machines.configurations.multiproc_dept_conf import MultiProcDeptConf
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
        self.multiproc_dept_conf = \
            MultiProcDeptConf(DefaultStationsConfigs.PIECES_TO_PRODUCE)

        # Instantiating MQTT objects
        self.mqtt_publisher = MqttPublisher('user:dept_manager/multiproc_dept')
        self.mqtt_conf_listener = MqttConfListener('multiproc_dept/conf', 
                                                   self.multiproc_dept_conf\
                                                    .to_object)
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

        # Process fields
        self.pieces_to_produce = DefaultStationsConfigs.PIECES_TO_PRODUCE
        self.pieces_completed = 0
        self.pieces_left = self.pieces_to_produce - self.pieces_completed
        self.process_completed = False
        self.to_reset = False

    def set_received_configuration(self, conf) -> None:
        self.logger.info('Saving the new configuration for {}'\
                         .format(self.dept_name))
        self.multiproc_dept_conf.pieces_to_produce = conf.pieces_to_produce
        self.pieces_to_produce = self.multiproc_dept_conf.pieces_to_produce
        self.pieces_left = self.pieces_to_produce - self.pieces_completed
    
    def read_all_sensors(self) -> None:
        self.oven_station.read_all_sensors()            # Oven station
        self.vacuum_gripper_carrier.read_all_sensors()  # Vacuum carrier  
        self.turntable_carrier.read_all_sensors()       # Turntable carrier
        # no senors!                                    # Saw station
        self.conveyor_carrier.read_all_sensors()        # Conveyor station
    
    def cleanup(self) -> None:
        """Cleanup function to leave the RevPi in a defined state."""
        self.logger.info('Cleaning the system state')

        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False                                     # type: ignore

        # - Turning off all the system actuators 
        # - Resetting stations states and 
        # - Closing MQTT connections
        self.compressor_service.deactivate_service()
        self.oven_station.deactivate_station()
        self.vacuum_gripper_carrier.deactivate_carrier()
        self.turntable_carrier.deactivate_carrier()
        self.saw_station.deactivate_station()
        self.conveyor_carrier.deactivate_carrier()

        # Closing the publisher MQTT connection
        self.mqtt_publisher.close_connection()
    
    def reset_station_states_and_stop(self) -> None:
        # - turning off all station actuators method;
        # - resetting station states method; 
        self.oven_station.reset_station()
        self.vacuum_gripper_carrier.reset_carrier()
        self.turntable_carrier.reset_carrier()
        self.saw_station.reset_station()
        self.conveyor_carrier.reset_carrier()
        self.compressor_service.turn_off_all_actuators()
        self.cleanup()
    
    def reset_station_states_and_restart(self) -> None: 
        # - turning off all station actuators method;
        # - resetting station states method; 
        self.oven_station.reset_station()
        self.vacuum_gripper_carrier.reset_carrier()
        self.turntable_carrier.reset_carrier()
        self.saw_station.reset_station()
        self.conveyor_carrier.reset_carrier()

    def start(self) -> None:        
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
            self.set_received_configuration(self.mqtt_conf_listener\
                                            .configuration)
            self.logger.info('New {} conf uploaded'\
                             .format(self.dept_name))
        else: 
            self.logger.info('No conf saved found, proceeding the standard '    
                             'conf for {}'.format(self.dept_name))
        
        # Activating the process services - i.e. the compressor_service
        self.compressor_service.activate_service()

        self.logger.info('Pieces to produce: {};'\
                         .format(self.pieces_to_produce))
        self.logger.info('Pieces completed {};'\
                         .format(self.pieces_completed))
        self.logger.info('Pieces left {};'\
                         .format(self.pieces_left))
        self.logger.info('Waiting for the first piece to process ...')

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 2 things, continuously: 
        #   1. Sets the Rpi a1 light
        #   2. Follows the process description
        # The cycle is set in ... .exitsignal.wait(0.05) every 0.05s
        while (self.rpi.exitsignal.wait(0.05) == False):
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
                    self.oven_station.oven_process_start()

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
                self.vacuum_gripper_carrier\
                    .transfer_product_from_oven_to_turntable()
                self.turntable_carrier.prod_on_carrier = True
                    
            # Turn the turntable towards the saw
            if (self.turntable_carrier.prod_on_carrier == True and
                self.turntable_carrier.process_completed == False):
                # Activate the turntable until it reaches the saw
                if (self.turntable_carrier.turntable_pos != 'saw' and
                    self.saw_station.process_completed == False):
                    self.turntable_carrier.transfer_product_to_saw()
                    self.saw_station.prod_under_saw = True

                # Activate the saw for the designed processing time
                if (self.turntable_carrier.turntable_pos == 'saw' and 
                    self.saw_station.process_completed == False):
                    self.saw_station.processing()
            
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
                self.pieces_completed += 1
                # Setting the process as completed
                self.process_completed = True
                self.to_reset = True
                # Print the process completion message
                self.logger.info('piece completed')
                self.pieces_left = self.pieces_to_produce - \
                    self.pieces_completed
                self.logger.info('{} pieces to be produced'\
                                 .format(self.pieces_to_produce))
                self.logger.info('{} pieces produced'\
                                 .format(self.pieces_completed))
                self.logger.info('{} pieces left to produce'\
                                 .format(self.pieces_left))

            ###################################################################
            # If the product is in moved from the conveyor light barrier, reset
            # everything, and set the dept as ready to restart
            if(self.conveyor_carrier.light_barrier_state == True 
               and self.process_completed == True
               and self.to_reset == True):
                if(self.pieces_completed == self.pieces_to_produce):
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
                    ('Waiting ...')

if __name__ == "__main__":
    # Instantiating the controlling class
    root = MultiprocessManager('multiproc_dept')
    # Launch the start function of the RevPi event control system
    root.start()
