#!/usr/bin/env python

# TODO: wrap the different class into a coherent subfolder structure
"""
process_actuator.py: ProcessActuator class

This class is aimed at controlling the whole Fischertechnik loop process.
It contains the RevPi mainloop, and every class used should be attached to this 
file.

The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2

from machines.compressor import Compressor
from machines.oven_station import OvenStation
from machines.vacuum_carrier import VacuumCarrier
from machines.turntable_carrier import TurntableCarrier
from machines.saw import Saw
from machines.conveyor import Conveyor

class ProcessActuator():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)
        
        # My aggregated objects
        self.oven = OvenStation(self.rpi)
        self.vacuum_gripper_carrier = VacuumCarrier(self.rpi)
        self.turntable_carrier = TurntableCarrier(self.rpi)
        self.saw_actuator = Saw(self.rpi)
        self.conveyor_carrier = Conveyor(self.rpi)

        self.compressor = \
            Compressor(self.rpi, 'Multistation Compressor', 10)   # TODO: evaluate class changing
        
        # Support time sensors 
        # TODO: evaluate if is worth to use all those vars or only one is enough
        # Saw process time counter
        self.time_sens_saw_count = 0
        # Oven process time counter
        self.time_sens_oven_count = 0
        # Vacuum process time counter
        self.time_sens_vacuum_count = 0
        # Delivery turntable pusher time counter
        self.time_sens_turntable_pusher_count = 0
        # Generic counter
        self.counter = 0
        

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program
        print('Cleaning the system state')
        self.rpi.core.a1green.value = False

        # TODO: implement pin reset from within the sensor/actuator class
        self.rpi.io['O_1'].value = False
        self.rpi.io['O_2'].value = False
        self.rpi.io['O_3'].value = False
        self.rpi.io['O_4'].value = False
        self.rpi.io['O_5'].value = False
        self.rpi.io['O_6'].value = False
        self.rpi.io['O_7'].value = False
        self.rpi.io['O_8'].value = False
        self.rpi.io['O_9'].value = False
        self.rpi.io['O_10'].value = False
        self.rpi.io['O_11'].value = False
        self.rpi.io['O_12'].value = False
        self.rpi.io['O_13'].value = False
        self.rpi.io['O_14'].value = False
        # Cleaning the object support states
        self.reset_station_states()
    
    def reset_station_states(self):
        # Support time sensors
        # TODO: evaluate if to use a single counter var
        self.time_sens_saw_count = 0
        self.time_sens_oven_count = 0
        self.time_sens_vacuum_count = 0
        self.time_sens_delivery_count = 0 
        self.time_sens_turntable_pusher_count = 0
        self.counter = 0

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
        # do other things
        self.rpi.core.a1green.value = not self.rpi.core.a1green.value
        
        # Activating the process services - i.e. the compressor
        self.compressor.turn_on()
        
        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 2 things, continuously: 
        #   1. Sets the Rpi a1 light
        #   2. Follows the process description
        while (self.rpi.exitsignal.wait(0.05) == False):
            # TODO: simplify the process loop
            # Follows the process description ###############################
            # If the oven-light sensor is False, that is there is the product
            # So, set the self.prod_on_oven_carrier to True
            if (self.oven.get_light_barrier_state() == False):
                self.oven.prod_on_carrier = True
            
            # If there is the product on the oven carrier, move the vacuum 
            # carrier towards the oven
            if (self.oven.process_completed == False and 
                self.oven.prod_on_carrier == True):
                # Move the carrier towards the oven
                if (self.vacuum_gripper_carrier.get_carrier_position() != 'oven'):
                    # Activate it towards the oven
                    self.vacuum_gripper_carrier.move_carrier_towards_oven()
                    
            # If the oven is not ready and the vacuum carrier grip is at the 
            # oven and the product is on the oven carrier: 
            if (self.oven.process_completed == False and
                self.oven.prod_on_carrier == True and 
                self.vacuum_gripper_carrier.get_carrier_position() == 'oven'):
                # Move inside the oven the oven carrier
                if (self.oven.get_carrier_position() == 'outside'):
                    self.oven.move_carrier_inward()
                else:
                    # TODO: modify so that the light flashes only AFTER the door is completely closed
                    #haha, flashing lights go brrrr - For light flashing
                    if (self.time_sens_oven_count % 2 == 1):
                        # Activate the process light
                        self.oven.activate_process_light()
                    else:
                        # Deactivate the process light
                        self.oven.deactivate_process_light()
                    # Time counter
                    self.time_sens_oven_count += 1            

                # If the counter reaches 30, stop the oven process
                if (self.time_sens_oven_count >= 30):       
                    # Deactivate the light
                    self.oven.deactivate_process_light()
                    # Set the oven process var to True
                    self.oven.process_completed = True
                    # Set the oven counter to 0
                    self.time_sens_oven_count = 0

            # If the oven is ready
            elif (self.oven.process_completed == True and 
                  self.oven.prod_on_carrier == True):
                # If oven_feeder_out sensor is False = the carrier is not 
                # out
                self.oven.move_carrier_outward()        

            # Take the product with the carrier grip
            # Lower the vacuum gripper
            # If oven feeder sensor is True and oven ready is True and the
            # vacuum gripper variable is True and vacuum counter is less
            # than 10, that is if the oven feeder is out from the oven and
            # the oven is in ready state and the vacuum carrieer gripper 
            # is at the oven and the vacuum counter is less than 10
            # The counter is needed in order to wait for the vacuum gripper
            # to be completely lowered  
            if (self.oven.get_carrier_position() == 'outside' 
                and self.oven.process_completed == True
                and self.vacuum_gripper_carrier.get_carrier_position() == 'oven' 
                and self.oven.prod_on_carrier == True):
                if (self.time_sens_vacuum_count < 10):
                    # Lower the carrier vacuum gripper
                    self.vacuum_gripper_carrier.lower_vac_gripper()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                # Grip the product 
                # If vacuum count is greater than 10 and less than 15
                if (self.time_sens_vacuum_count >= 10 and 
                    self.time_sens_vacuum_count < 15):
                    # Activate the carrier vacuum gripper
                    self.vacuum_gripper_carrier.grip_object()
                    # Add 1 to the vacuum count
                    self.time_sens_vacuum_count += 1

                # Raise the vacuum gripper 
                # If vacuum count is greater than 15 and less than 25
                if (self.time_sens_vacuum_count >= 15 and 
                        self.time_sens_vacuum_count < 35):
                    # Upper the carrier vacuum gripper
                    self.vacuum_gripper_carrier.raise_vac_gripper()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                if(self.vacuum_gripper_carrier.get_carrier_position() == 'oven'
                    and self.vacuum_gripper_carrier.get_vac_position() == 'high'
                    and self.vacuum_gripper_carrier.get_gripper_state() == 'activated'
                    and self.time_sens_vacuum_count >= 25):
                    self.time_sens_vacuum_count = 0
                    self.oven.prod_on_carrier = False
                    self.vacuum_gripper_carrier.prod_on_carrier = True
            
            # Move the carrier to the turnta#ble
            if (self.vacuum_gripper_carrier.prod_on_carrier == True and
                self.vacuum_gripper_carrier.get_carrier_position() != 'turntable'):
                # Bring the carrier vacuum gripper to the turn-table
                self.vacuum_gripper_carrier.move_carrier_towards_turntable()

            # Release the product
            # Lower the carrier vacuum gripper
            if (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                and self.vacuum_gripper_carrier.prod_on_carrier == True
                and self.vacuum_gripper_carrier.get_gripper_state() == 'activated'
                and self.time_sens_vacuum_count < 15):
                    self.vacuum_gripper_carrier.lower_vac_gripper()
                    self.time_sens_vacuum_count += 1
                    
            # Release the product on the turntable
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                  and self.vacuum_gripper_carrier.get_vac_position() == 'low'
                  and self.time_sens_vacuum_count >= 15 
                  and self.time_sens_vacuum_count < 30):
                    self.vacuum_gripper_carrier.release_object()
                    self.time_sens_vacuum_count += 1

            # Raise the carrier vacuum gripper
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                  and self.vacuum_gripper_carrier.get_vac_position() == 'low' 
                  and self.vacuum_gripper_carrier.get_gripper_state() == 'deactivated'
                  and self.time_sens_vacuum_count >= 30):
                    self.time_sens_vacuum_count = 0
                    self.vacuum_gripper_carrier.raise_vac_gripper()
                    self.vacuum_gripper_carrier.prod_on_carrier = False
                    self.vacuum_gripper_carrier.process_completed = True
                    self.turntable_carrier.prod_on_carrier = True

            # Turn the turntable towards the saw
            if (self.turntable_carrier.prod_on_carrier == True and
                self.turntable_carrier.process_completed == False):
                # Activate the turntable until it reaches the saw
                if (self.turntable_carrier.get_carrier_position() != 'saw' and
                    self.saw_actuator.process_completed == False):
                    self.turntable_carrier.rotate_towards_saw()

                # Activate the saw for the design processing time
                if (self.turntable_carrier.get_carrier_position() == 'saw' and
                    self.saw_actuator.process_completed == False and
                    self.time_sens_saw_count < 40):
                    self.saw_actuator.activate_saw()
                    self.time_sens_saw_count += 1
                elif (self.turntable_carrier.get_carrier_position() == 'saw' and 
                    self.saw_actuator.process_completed == False and
                    self.time_sens_saw_count >= 40): 
                    self.saw_actuator.deactivate_saw()
                    self.saw_actuator.process_completed = True
                    self.time_sens_saw_count = 0
            
                # Activate the turntable until it reaches the conveyor                
                if (self.saw_actuator.process_completed == True and
                    self.turntable_carrier.get_carrier_position() != 'conveyor'):                    
                    self.turntable_carrier.rotate_towards_conveyor()
            
                # Activate the pusher
                if (self.turntable_carrier.get_carrier_position() == 'conveyor' and
                    self.time_sens_turntable_pusher_count < 20):
                    self.turntable_carrier.activate_pusher()
                    self.time_sens_turntable_pusher_count += 1
                elif(self.turntable_carrier.get_carrier_position() == 'conveyor' and
                    self.time_sens_turntable_pusher_count >= 20):
                    self.turntable_carrier.deactivate_pusher()
                    self.turntable_carrier.prod_on_carrier = False
                    self.turntable_carrier.process_completed = True
                    self.conveyor_carrier.prod_on_conveyor = True
                    self.time_sens_turntable_pusher_count = 0
            
            # Activate the conveyor
            if (self.conveyor_carrier.prod_on_conveyor == True
                and self.conveyor_carrier.process_completed == False):
                if (self.conveyor_carrier.get_ligth_barrier_state() == 'free'):
                    self.conveyor_carrier.move_to_the_exit()
                if (self.conveyor_carrier.get_ligth_barrier_state() == 'occupied'):
                    self.conveyor_carrier.process_completed = True

            #################################################################
            # Otherwise, if there is the product in front of the light sensor
            if(self.conveyor_carrier.get_ligth_barrier_state() == 'occupied' 
               and self.conveyor_carrier.process_completed == True 
               and self.turntable_carrier.process_completed == True 
               and self.saw_actuator.process_completed == True 
               and self.vacuum_gripper_carrier.process_completed == True 
               and self.oven.process_completed == True):
                # Turn off the services
                self.compressor.turn_off()
                
                # Turn off the valve feeder
                self.turntable_carrier.deactivate_pusher()
                # Turn off the conveyor belt
                self.conveyor_carrier.deactivate_carrier()
                # Turn the turn-table towards the carrier
                # If the turntable_pos_vacuum sensor is False, that is 
                # if the turntable is not at the vacuum gripper carrier
                if (self.turntable_carrier.get_carrier_position() != 'vacuum carrier'):
                    # Activate the conveyor rotation clockwise
                    self.turntable_carrier.rotate_towards_vacuum_carrier()

                # Finally, reset the counters
                self.reset_station_states()


if __name__ == "__main__":
    # Instantiating the controlling class
    root = ProcessActuator()
    # Launch the start function of the RevPi event control system
    root.start()
