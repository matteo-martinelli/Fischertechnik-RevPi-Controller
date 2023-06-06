#!/usr/bin/env python

"""
multiprocess_manager.py: MultiprocessManager class

This class is aimed at controlling the whole Fischertechnik loop process.
It contains the RevPi mainloop, and every class used should be attached to this 
file.

The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""

# TODO: aggiungi pubblicazione dei sensori solo se è cambiato dall'ultimo valore.

import revpimodio2
import time

from mqtt_publisher import MqttPublisher

from machines.compressor_service import CompressorService
from machines.oven_station import OvenStation
from machines.vacuum_carrier import VacuumCarrier
from machines.turntable_carrier import TurntableCarrier
from machines.saw_station import SawStation
from machines.conveyor_carrier import ConveyorCarrier


class MultiprocessManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self, dept_name):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup)

        # Instantiating the MQTT publisher
        self.mqtt_publisher = MqttPublisher()
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
                              10, self.mqtt_publisher) # TODO: evaluate class changing
        
        # Process fields
        self.piece_counter = 0
        self.process_completed = False
        self.to_reset = False        

    def cleanup(self):
        """Cleanup function to leave the RevPi in a defined state."""
        print('Cleaning the system state')

        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False
        
        # Closing the MQTT connection
        self.mqtt_publisher.close_connection()

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
        self.oven_station.deactivate_station()
        self.vacuum_gripper_carrier.deactivate_carrier()
        self.turntable_carrier.deactivate_carrier()
        self.saw_station.deactivate_station()
        self.conveyor_carrier.deactivate_carrier()

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
        # do other things
        self.rpi.core.a1green.value = not self.rpi.core.a1green.value

        # Connecting to the MQTT broker
        self.mqtt_publisher.open_connection()
        
        # Activating the process services - i.e. the compressor_service
        self.compressor_service.activate_service()

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 2 things, continuously: 
        #   1. Sets the Rpi a1 light
        #   2. Follows the process description
        # The cycle is set in ... .exitsignal.wait(0.05) every 0.05s
        while (self.rpi.exitsignal.wait(0.05) == False):
            # TODO: simplify the process loop
            # First things first: reading all the sensors states
            
            # Oven station
            self.oven_station.read_sensors()

            # Vacuum carrier
            self.vacuum_gripper_carrier.read_sensors()

            # Turntable carrier
            self.turntable_carrier.read_sensors()
            
            # Saw station
            # no senors!
            
            # Conveyor station
            self.conveyor_carrier.read_sensors()
            #self.conveyor_carrier.read_actuators()

            # TODO: add a "update all sensors" method to all the involved classes;
            # TODO: this method will be called here. 
            # TODO: evaluate the update all behaviour

            # TODO: update deactivate_station methods with gets and sets from classes.
            # TODO: change sensor setters into readers
            # Follows the process description #################################
            # If the oven_station-light sensor is False, that is there is the 
            # product. So, set the self.prod_on_oven_station_carrier to True
            if (self.oven_station.get_light_barrier_state() == False):
                self.oven_station.set_prod_on_carrier(True)

            # If there is the product on the oven_station carrier, move the 
            # vacuum carrier towards the oven_station
            if (self.oven_station.get_process_completed() == False and 
                self.oven_station.get_prod_on_carrier() == True):
                # Move the carrier towards the oven_station
                if (self.vacuum_gripper_carrier.get_carrier_position() 
                    != 'oven'):
                    # Activate it towards the oven_station
                    self.vacuum_gripper_carrier.move_carrier_towards_oven()
                    
            # If the oven_station is not ready and the vacuum carrier grip is 
            # at the oven_station and the product is on the oven_station 
            # carrier: 
            if (self.oven_station.get_process_completed() == False and
                self.oven_station.get_prod_on_carrier() == True and 
                self.vacuum_gripper_carrier.get_carrier_position() == 'oven'):
                # Move inside the oven_station the oven_station carrier
                if (self.oven_station.get_carrier_position() == 'outside'):
                    self.oven_station.move_carrier_inward()
                
                # When the carrier is inside the oven_station
                if (self.oven_station.get_carrier_position() == 'inside'):
                    self.oven_station.oven_process_start(3) # Time in seconds
                    self.oven_station.set_process_completed(True)

                # When the oven_station process is completed
                if (self.oven_station.get_process_completed() == True and 
                    self.oven_station.get_prod_on_carrier() == True):
                    # If oven_station_feeder_out sensor is False = the carrier 
                    # is not out
                    self.oven_station.move_carrier_outward()        

            # Take the product with the carrier grip
            # Lower the vacuum gripper
            # If oven_station feeder sensor is True and oven_station ready is 
            # True and the vacuum gripper variable is True and vacuum counter 
            # is less than 10, that is if the oven_station feeder is out from 
            # the oven_station and the oven_station is in ready state and the 
            # vacuum carrieer gripper is at the oven_station and the vacuum 
            # counter is less than 10 The counter is needed in order to wait 
            # for the vacuum gripper to be completely lowered  
            if (self.oven_station.get_carrier_position() == 'outside' and 
                self.oven_station.get_process_completed() == True and
                self.oven_station.get_prod_on_carrier() == True and
                self.vacuum_gripper_carrier.get_carrier_position() == 'oven'):
                
                self.vacuum_gripper_carrier.lower_gripper(1)

                self.vacuum_gripper_carrier.activate_gripper()
            
                self.vacuum_gripper_carrier.higher_gripper()

                # Set the gripping process as completed
                if(self.vacuum_gripper_carrier.get_carrier_position() == 'oven'
                    and self.vacuum_gripper_carrier.
                    get_gripper_lowering_state() == False
                    and self.vacuum_gripper_carrier.
                    get_gripper_activation_state() == True 
                    ):
                    self.oven_station.set_prod_on_carrier(False)
                    self.vacuum_gripper_carrier.set_prod_on_carrier(True)
                
            # Move the carrier to the turntable
            if (self.vacuum_gripper_carrier.get_prod_on_carrier() == True and
                self.vacuum_gripper_carrier.get_carrier_position() != 
                'turntable'):
                # Bring the carrier vacuum gripper to the turn-table
                self.vacuum_gripper_carrier.move_carrier_towards_turntable()

            # Release the product
            # Lower the carrier vacuum gripper
            if (self.vacuum_gripper_carrier.get_carrier_position() == 
                'turntable'
                and self.vacuum_gripper_carrier.get_prod_on_carrier() == True
                and self.vacuum_gripper_carrier.get_gripper_activation_state() 
                == True ):
                    self.vacuum_gripper_carrier.lower_gripper(0.5)
                    self.vacuum_gripper_carrier.deactivate_gripper()
                    time.sleep(1) # TODO: Add this sleep into deactivate_gripper(waiting_time)

            # Raise the carrier vacuum gripper
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 
                  'turntable'
                  and self.vacuum_gripper_carrier.
                  get_gripper_lowering_state() == True 
                  and self.vacuum_gripper_carrier.
                  get_gripper_activation_state() == False):
                    self.vacuum_gripper_carrier.higher_gripper()
                    self.vacuum_gripper_carrier.set_prod_on_carrier(False)
                    self.vacuum_gripper_carrier.set_process_completed(True)
                    self.turntable_carrier.set_prod_on_carrier(True)

            # Turn the turntable towards the saw
            if (self.turntable_carrier.get_prod_on_carrier() == True and
                self.turntable_carrier.get_process_completed() == False):
                # Activate the turntable until it reaches the saw
                if (self.turntable_carrier.get_carrier_position() != 'saw' and
                    self.saw_station.get_process_completed() == False):
                    self.turntable_carrier.rotate_towards_saw()
                    self.saw_station.set_prod_under_saw(True)

                # Activate the saw for the design processing time
                if (self.turntable_carrier.get_carrier_position() == 'saw' 
                    and self.saw_station.get_process_completed() == False):
                    self.saw_station.processing(2)
                    self.saw_station.set_process_completed(True)
            
                # Activate the turntable until it reaches the conveyor                
                if (self.saw_station.get_process_completed() == True and
                    self.turntable_carrier.get_carrier_position() != 
                    'conveyor'):                    
                    self.saw_station.set_prod_under_saw(False)
                    self.turntable_carrier.rotate_towards_conveyor()
            
                # Activate the pusher
                if (self.turntable_carrier.get_carrier_position() == 
                    'conveyor'):
                    self.turntable_carrier.activate_pusher(1)
                    self.turntable_carrier.deactivate_pusher()
                    self.turntable_carrier.set_prod_on_carrier(False)
                    self.turntable_carrier.set_process_completed(True)
                    self.conveyor_carrier.set_prod_on_conveyor(True)
                    self.turntable_carrier.rotate_towards_vacuum_carrier()
            
            # Activate the conveyor
            if (self.conveyor_carrier.get_prod_on_conveyor() == True
                and self.conveyor_carrier.get_process_completed() == False):
                # Move towards exit
                if (self.conveyor_carrier.get_light_barrier_state() == True):
                    self.conveyor_carrier.move_to_the_exit()
                # Once at the exit, set the process as completed
                if (self.conveyor_carrier.get_light_barrier_state() == False):
                    self.conveyor_carrier.set_process_completed(True)
                    
            ###################################################################
            # If there is the product in front of the light sensor
            if(self.conveyor_carrier.get_light_barrier_state() == False 
               and self.conveyor_carrier.get_process_completed() == True 
               and self.turntable_carrier.get_process_completed() == True 
               and self.saw_station.get_process_completed() == True 
               and self.vacuum_gripper_carrier.get_process_completed() == True 
               and self.oven_station.get_process_completed() == True
               and self.process_completed == False):
                # Print the process completion message
                print('process completed')
                # Add 1 to the piece counter
                self.piece_counter += 1
                # Setting the process as completed
                self.process_completed = True
                self.to_reset = True

            ###################################################################
            # If the product is in moved from the conveyor light barrier, reset
            # everything, and set the dept as ready to restart
            if(self.conveyor_carrier.get_light_barrier_state() == True 
               and self.process_completed == True
               and self.to_reset == True):
                # Print the process completion message
                print('resetting the dept')
                # Reset the system
                self.conveyor_carrier.set_prod_on_conveyor(False)
                self.reset_station_states_and_restart()
                self.to_reset = False

if __name__ == "__main__":
    # Instantiating the controlling class
    root = MultiprocessManager('multiproc_dept')
    # Launch the start function of the RevPi event control system
    root.start()
