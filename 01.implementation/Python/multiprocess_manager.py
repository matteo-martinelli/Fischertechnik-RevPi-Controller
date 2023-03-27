#!/usr/bin/env python

# TODO: convert all the class functions from camel to snake case
"""
process_actuator.py: ProcessManager class

This class is aimed at controlling the whole Fischertechnik loop process.
It contains the RevPi mainloop, and every class used should be attached to this 
file.

The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2

from mqtt_publisher import MqttPublisher

from machines.compressor import Compressor
from machines.oven_station import OvenStation
from machines.vacuum_carrier import VacuumCarrier
from machines.turntable_carrier import TurntableCarrier
from machines.saw import Saw
from machines.conveyor import Conveyor


class MultiprocessManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)

        # Instantiating the MQTT publisher
        self.mqtt_publisher = MqttPublisher()
        
        # My aggregated objects
        self.oven = OvenStation(self.rpi)
        self.vacuum_gripper_carrier = VacuumCarrier(self.rpi)
        self.turntable_carrier = TurntableCarrier(self.rpi)
        self.saw_actuator = Saw(self.rpi)
        self.conveyor_carrier = Conveyor(self.rpi)

        self.compressor = Compressor(self.rpi, 10)   # TODO: evaluate class changing
        
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
        print('Cleaning the system state')

        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False
        
        # Closing the MQTT connection
        self.mqtt_publisher.close_connection()

        # Turning off all the system actuators
        self.compressor.motor.turn_off()
        self.oven.oven_carrier.turn_off()
        self.turntable_carrier.motor.turn_off()
        self.saw_actuator.motor.turn_off()
        self.conveyor_carrier.motor.turn_off()

        # Cleaning the object support states
        self.reset_station_states()
    
    def reset_station_states(self):
        # Support time sensors
        self.time_sens_saw_count = 0
        self.time_sens_oven_count = 0
        self.time_sens_vacuum_count = 0
        self.time_sens_delivery_count = 0 
        self.time_sens_turntable_pusher_count = 0
        self.counter = 0
        # Objects process completed flags
        self.oven.process_completed = False
        self.conveyor_carrier.process_completed = False
        self.turntable_carrier.process_completed = False
        self.saw_actuator.process_completed = False
        self.conveyor_carrier.process_completed = False

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
        
        # Activating the process services - i.e. the compressor
        #self.compressor.motor.turn_on()
        self.compressor.activate()

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
            if (self.oven.light_barrier.get_state() == False):
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
                
                # When the carrier is inside the oven
                if (self.oven.get_carrier_position() == 'inside'):
                    #haha, flashing lights go brrrr - For light flashing
                    if (self.time_sens_oven_count % 2 == 1):
                        # Activate the process light
                        self.oven.oven_proc_light.turn_on()
                    else:
                        # Deactivate the process light
                        self.oven.oven_proc_light.turn_off()
                    # Time counter
                    self.time_sens_oven_count += 1            

                # When the counter reaches 30, stop the oven process
                if (self.time_sens_oven_count >= 30):       
                    # Deactivate the light
                    self.oven.oven_proc_light.turn_off()
                    # Set the oven process var to True
                    self.oven.process_completed = True
                    # Set the oven counter to 0
                    self.time_sens_oven_count = 0

                # When the oven process is completed
                if (self.oven.process_completed == True and 
                    self.oven.prod_on_carrier == True):
                    # If oven_feeder_out sensor is False = the carrier is not out
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
                
                # Lower the vacuum gripper
                if (self.time_sens_vacuum_count < 10):
                    # Lower the carrier vacuum gripper
                    self.vacuum_gripper_carrier.gripper_lowering.turn_on()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                # Grip the product 
                # If vacuum count is greater than 10 and less than 15
                if (self.time_sens_vacuum_count >= 10 and 
                    self.time_sens_vacuum_count < 15):
                    # Activate the carrier vacuum gripper
                    self.vacuum_gripper_carrier.gripper_activation.turn_on()
                    # Add 1 to the vacuum count
                    self.time_sens_vacuum_count += 1

                # Raise the vacuum gripper 
                # If vacuum count is greater than 15 and less than 25
                if (self.time_sens_vacuum_count >= 15 and 
                        self.time_sens_vacuum_count < 35):
                    # Upper the carrier vacuum gripper
                    self.vacuum_gripper_carrier.gripper_lowering.turn_off()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1

                # Set the gripping process as completed
                if(self.vacuum_gripper_carrier.get_carrier_position() == 'oven'
                    and self.vacuum_gripper_carrier.gripper_lowering.get_state() == False
                    and self.vacuum_gripper_carrier.gripper_activation.get_state() == True
                    and self.time_sens_vacuum_count >= 35):
                    self.time_sens_vacuum_count = 0
                    self.oven.prod_on_carrier = False
                    self.vacuum_gripper_carrier.prod_on_carrier = True
                
            # Move the carrier to the turntable
            if (self.vacuum_gripper_carrier.prod_on_carrier == True and
                self.vacuum_gripper_carrier.get_carrier_position() != 'turntable'):
                # Bring the carrier vacuum gripper to the turn-table
                self.vacuum_gripper_carrier.move_carrier_towards_turntable()

            # Release the product
            # Lower the carrier vacuum gripper
            if (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                and self.vacuum_gripper_carrier.prod_on_carrier == True
                and self.vacuum_gripper_carrier.gripper_activation.get_state() == True
                and self.time_sens_vacuum_count < 15):
                    self.vacuum_gripper_carrier.gripper_lowering.turn_on()
                    self.time_sens_vacuum_count += 1
                    
            # Release the product on the turntable
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                  and self.vacuum_gripper_carrier.gripper_lowering.get_state() == True
                  and self.time_sens_vacuum_count >= 15 
                  and self.time_sens_vacuum_count < 30):
                    self.vacuum_gripper_carrier.gripper_activation.turn_off()
                    self.time_sens_vacuum_count += 1

            # Raise the carrier vacuum gripper
            elif (self.vacuum_gripper_carrier.get_carrier_position() == 'turntable'
                  and self.vacuum_gripper_carrier.gripper_lowering.get_state() == True 
                  and self.vacuum_gripper_carrier.gripper_activation.get_state() == False
                  and self.time_sens_vacuum_count >= 30):
                    self.time_sens_vacuum_count = 0
                    self.vacuum_gripper_carrier.gripper_lowering.turn_off()
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
                if (self.turntable_carrier.get_carrier_position() == 'saw' 
                    and self.saw_actuator.process_completed == False and
                    self.time_sens_saw_count < 40):
                    self.saw_actuator.motor.turn_on()
                    self.time_sens_saw_count += 1
                elif (self.turntable_carrier.get_carrier_position() == 'saw' 
                      and self.saw_actuator.process_completed == False and
                    self.time_sens_saw_count >= 40): 
                    self.saw_actuator.motor.turn_off()
                    self.saw_actuator.process_completed = True
                    self.time_sens_saw_count = 0
            
                # Activate the turntable until it reaches the conveyor                
                if (self.saw_actuator.process_completed == True and
                    self.turntable_carrier.get_carrier_position() != 'conveyor'):                    
                    self.turntable_carrier.rotate_towards_conveyor()
            
                # Activate the pusher
                if (self.turntable_carrier.get_carrier_position() == 'conveyor' and
                    self.time_sens_turntable_pusher_count < 20):
                    self.turntable_carrier.pusher_activation.turn_on()
                    self.time_sens_turntable_pusher_count += 1
                # Deactivate the pusher and rotate the turntable to the 
                # conveyor
                elif(self.turntable_carrier.get_carrier_position() == 'conveyor' and
                    self.time_sens_turntable_pusher_count >= 20):
                    self.turntable_carrier.pusher_activation.turn_off()
                    self.turntable_carrier.prod_on_carrier = False
                    self.turntable_carrier.process_completed = True
                    self.conveyor_carrier.prod_on_conveyor = True
                    self.time_sens_turntable_pusher_count = 0
            
            # Activate the conveyor
            if (self.conveyor_carrier.prod_on_conveyor == True
                and self.conveyor_carrier.process_completed == False):
                if (self.conveyor_carrier.light_barrier.get_state() == True):
                    self.conveyor_carrier.move_to_the_exit()
                if (self.conveyor_carrier.light_barrier.get_state() == False):
                    self.conveyor_carrier.process_completed = True

            #################################################################
            # If there is the product in front of the light sensor
            if(self.conveyor_carrier.light_barrier.get_state() == False 
               and self.conveyor_carrier.process_completed == True 
               and self.turntable_carrier.process_completed == True 
               and self.saw_actuator.process_completed == True 
               and self.vacuum_gripper_carrier.process_completed == True 
               and self.oven.process_completed == True):
                
                # Turn off the valve feeder
                self.turntable_carrier.pusher_activation.turn_off()
                # Turn off the conveyor belt
                self.conveyor_carrier.motor.turn_off()
                # Turn the turn-table towards the carrier
                self.turntable_carrier.rotate_towards_vacuum_carrier()
                
            #################################################################
            # If the product is in moved from the conveyor light barrier, reset
            # everything
            if(self.conveyor_carrier.light_barrier.get_state() == True 
               and self.conveyor_carrier.process_completed == True 
               and self.turntable_carrier.process_completed == True 
               and self.saw_actuator.process_completed == True 
               and self.vacuum_gripper_carrier.process_completed == True 
               and self.oven.process_completed == True):
                self.conveyor_carrier.prod_on_conveyor = False
                self.reset_station_states()
                    
if __name__ == "__main__":
    # Instantiating the controlling class
    root = MultiprocessManager()
    # Launch the start function of the RevPi event control system
    root.start()
