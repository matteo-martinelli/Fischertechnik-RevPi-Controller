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

from mqtt_publisher import MqttPublisher

from datetime import datetime  

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
                                    # TODO: set as a mqtt pub field
        
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
        
        # Support time sensors 
        # TODO: evaluate if is worth to use all those vars or only one is enough
        # Saw process time timer
        self.time_sens_saw_timer = 0
        # oven_station process time timer
        self.time_sens_oven_station_timer = 0
        # Vacuum process time timer
        self.time_sens_vacuum_timer = 0
        # Delivery turntable pusher timer
        self.time_sens_turntable_pusher_timer = 0
        # Generic timer
        self.timer = 0
        

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
        #self.compressor_service.deactivate_service()
        self.oven_station.deactivate_station()
        self.vacuum_gripper_carrier.deactivate_carrier()
        self.turntable_carrier.deactivate_carrier()
        self.saw_station.deactivate_station()
        self.conveyor_carrier.deactivate_carrier()

        # Support time sensors
        self.time_sens_saw_timer = 0
        self.time_sens_oven_station_timer = 0
        self.time_sens_vacuum_timer = 0
        self.time_sens_delivery_count = 0 
        self.time_sens_turntable_pusher_timer = 0
        self.timer = 0
        # Objects process completed flags
        #self.oven_station.process_completed = False
        #self.conveyor_carrier.process_completed = False
        #self.turntable_carrier.process_completed = False
        #self.saw_station.process_completed = False
        #self.conveyor_carrier.process_completed = False

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
        #self.compressor_service.motor.turn_on()
        self.compressor_service.activate_service()
        #self.mqtt_publisher.publish_telemetry_data(
        #    'proc_dept/services/compressor_service/telemetry', 
        #    self.compressor_service.motor.to_json())

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 2 things, continuously: 
        #   1. Sets the Rpi a1 light
        #   2. Follows the process description
        # The cycle is set in ... .exitsignal.wait(0.05) every 0.05s
        while (self.rpi.exitsignal.wait(0.05) == False):
            # TODO: simplify the process loop
            # Follows the process description ###############################
            # If the oven_station-light sensor is False, that is there is the product
            # So, set the self.prod_on_oven_station_carrier to True
            if (self.oven_station.get_light_barrier_state() == False):
                self.oven_station.set_prod_on_carrier(True)

            # If there is the product on the oven_station carrier, move the vacuum 
            # carrier towards the oven_station
            if (self.oven_station.get_process_completed() == False and 
                self.oven_station.get_prod_on_carrier() == True):
                # Move the carrier towards the oven_station
                if (self.vacuum_gripper_carrier.get_carrier_position() != 'oven'):
                    # Activate it towards the oven_station
                    self.vacuum_gripper_carrier.move_carrier_towards_oven()
            # If the oven_station is not ready and the vacuum carrier grip is at the 
            # oven_station and the product is on the oven_station carrier: 
            if (self.oven_station.get_process_completed() == False and
                self.oven_station.get_prod_on_carrier() == True and 
                self.vacuum_gripper_carrier.get_carrier_position() == 'oven'):
                # Move inside the oven_station the oven_station carrier
                if (self.oven_station.get_carrier_position() == 'outside'):
                    self.oven_station.move_carrier_inward()
                
                # When the carrier is inside the oven_station
                if (self.oven_station.get_carrier_position() == 'inside'):
                    # Turn on the oven_station light
                    self.oven_station.activate_proc_light()
                    # Time counter
                    self.time_sens_oven_station_timer += 1            

                # When the counter reaches 30, stop the oven_station process
                if (self.time_sens_oven_station_timer >= 30):       
                    # Deactivate the light
                    self.oven_station.deactivate_proc_light()
                    # Set the oven_station process var to True
                    self.oven_station.set_process_completed(True)
                    # Set the oven_station counter to 0
                    self.time_sens_oven_station_timer = 0

                # When the oven_station process is completed
                if (self.oven_station.get_process_completed() == True and 
                    self.oven_station.get_prod_on_carrier() == True):
                    # If oven_station_feeder_out sensor is False = the carrier is not out
                    self.oven_station.move_carrier_outward()        

            # Take the product with the carrier grip
            # Lower the vacuum gripper
            # If oven_station feeder sensor is True and oven_station ready is True and the
            # vacuum gripper variable is True and vacuum counter is less
            # than 10, that is if the oven_station feeder is out from the oven_station and
            # the oven_station is in ready state and the vacuum carrieer gripper 
            # is at the oven_station and the vacuum counter is less than 10
            # The counter is needed in order to wait for the vacuum gripper
            # to be completely lowered  
            if (self.oven_station.get_carrier_position() == 'outside' and 
                self.oven_station.get_process_completed() == True and
                self.oven_station.get_prod_on_carrier() == True and
                self.vacuum_gripper_carrier.get_carrier_position() == 'oven'):
                
                # Lower the vacuum gripper
                if (self.time_sens_vacuum_timer < 10):
                    # Lower the carrier vacuum gripper
                    self.vacuum_gripper_carrier.lower_gripper()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_timer += 1
            
                # Grip the product 
                # If vacuum count is greater than 10 and less than 15
                if (self.time_sens_vacuum_timer >= 10 and 
                    self.time_sens_vacuum_timer < 15):
                    # Activate the carrier vacuum gripper
                    self.vacuum_gripper_carrier.activate_gripper()
                    # Add 1 to the vacuum count
                    self.time_sens_vacuum_timer += 1

                # Raise the vacuum gripper 
                # If vacuum count is greater than 15 and less than 25
                if (self.time_sens_vacuum_timer >= 15 and 
                        self.time_sens_vacuum_timer < 35):
                    # Upper the carrier vacuum gripper
                    self.vacuum_gripper_carrier.higher_gripper()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_timer += 1

                # Set the gripping process as completed
                if(self.vacuum_gripper_carrier.get_carrier_position() == 'oven'
                    and self.vacuum_gripper_carrier.get_gripper_lowering_state() == False
                    and self.vacuum_gripper_carrier.get_gripper_activation_state() == True
                    and self.time_sens_vacuum_timer >= 35):
                    self.time_sens_vacuum_timer = 0
                    self.oven_station.set_prod_on_carrier(False)
                    self.vacuum_gripper_carrier.set_prod_on_carrier(True)
                
            # Move the carrier to the turntable
            if (self.vacuum_gripper_carrier.get_prod_on_carrier() == True and
                self.vacuum_gripper_carrier.get_carrier_position() != 'turntable'):
                # Bring the carrier vacuum gripper to the turn-table
                self.vacuum_gripper_carrier.move_carrier_towards_turntable()

            # Release the product
            # Lower the carrier vacuum gripper
            if (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                and self.vacuum_gripper_carrier.get_prod_on_carrier() == True
                and self.vacuum_gripper_carrier.get_gripper_activation_state() == True
                and self.time_sens_vacuum_timer < 15):
                    self.vacuum_gripper_carrier.lower_gripper()
                    self.time_sens_vacuum_timer += 1
                    
            # Release the product on the turntable
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                  and self.vacuum_gripper_carrier.get_gripper_lowering_state() == True
                  and self.time_sens_vacuum_timer >= 15 
                  and self.time_sens_vacuum_timer < 30):
                    self.vacuum_gripper_carrier.deactivate_gripper()
                    self.time_sens_vacuum_timer += 1

            # Raise the carrier vacuum gripper
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                  and self.vacuum_gripper_carrier.get_gripper_lowering_state() == True 
                  and self.vacuum_gripper_carrier.get_gripper_activation_state() == False
                  and self.time_sens_vacuum_timer >= 30):
                    self.time_sens_vacuum_timer = 0
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
                    and self.saw_station.get_process_completed() == False and
                    self.time_sens_saw_timer < 40):
                    self.saw_station.activate_saw()
                    self.time_sens_saw_timer += 1
                elif (self.turntable_carrier.get_carrier_position() == 'saw' 
                      and self.saw_station.get_process_completed() == False and
                    self.time_sens_saw_timer >= 40): 
                    self.saw_station.deactivate_saw()
                    self.saw_station.set_process_completed(True)
                    self.time_sens_saw_timer = 0
            
                # Activate the turntable until it reaches the conveyor                
                if (self.saw_station.get_process_completed() == True and
                    self.turntable_carrier.get_carrier_position() != 'conveyor'):                    
                    self.saw_station.set_prod_under_saw(False)
                    self.turntable_carrier.rotate_towards_conveyor()
            
                # Activate the pusher
                if (self.turntable_carrier.get_carrier_position() == 'conveyor' and
                    self.time_sens_turntable_pusher_timer < 20):
                    self.turntable_carrier.activate_pusher()
                    self.time_sens_turntable_pusher_timer += 1
                # Deactivate the pusher and rotate the turntable to the 
                # conveyor
                elif(self.turntable_carrier.get_carrier_position() == 'conveyor' and
                    self.time_sens_turntable_pusher_timer >= 20):
                    self.turntable_carrier.deactivate_pusher()
                    self.turntable_carrier.set_prod_on_carrier(False)
                    self.turntable_carrier.set_process_completed(True)
                    self.conveyor_carrier.set_prod_on_conveyor(True)
                    self.time_sens_turntable_pusher_timer = 0
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
                    
            #################################################################
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

            #################################################################
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
