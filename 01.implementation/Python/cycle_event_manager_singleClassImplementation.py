#!/usr/bin/env python

"""
cycle_event_manager.py: CycleEventManagerRevPi class

This class is aimed at controlling the whole Fischertechnik loop process. 
The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
from compressor import Compressor
from light_barrier import LightBarrier
from reference_switch import ReferenceSwitch
from single_motion_actuator import SingleMotionActuator
from double_motion_actuator import DoubleMotionActuator
from vacuum_actuator import VacuumActuator


class CycleEventManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)
        
        # My actuator objects
        self.turntable = \
            DoubleMotionActuator(self.rpi, 'Turntable act', 1, 2)
        self.conveyor = \
            SingleMotionActuator(self.rpi, 'Conveyor act', 3)
        self.saw = \
            SingleMotionActuator(self.rpi, 'Saw act', 4)
        self.oven_carrier = \
            DoubleMotionActuator(self.rpi, 'Oven carrier act', 5, 6)
        self.vacuum_carrier = \
            DoubleMotionActuator(self.rpi, 'Vacuum carrier act', 7, 8)
        self.oven_proc_light = \
            SingleMotionActuator(self.rpi, 'Oven proc light act', 9)
        self.compressor = \
            Compressor(self.rpi, 'Multistation Compressor', 10)   # TODO: evaluate class changing
        self.vacuum_valve_grip = \
            SingleMotionActuator(self.rpi, 'Vacuum valve grip act', 11)
        self.vacuum_grip_lowering = \
            SingleMotionActuator(self.rpi, 'Vacuum grip lowering act', 12)
        self.oven_door_opening = \
            SingleMotionActuator(self.rpi, 'Oven door opening act', 13)
        self.turntable_pusher = \
            SingleMotionActuator(self.rpi, 'Turntable pusher act', 14)

        # My sensor objects
        self.turntab_under_vacuum_switch = \
            ReferenceSwitch(self.rpi, 'turntable under vacuum switch', 1)
        self.turntab_towards_conveyor_switch = \
            ReferenceSwitch(self.rpi, 'turntable towards conveyor switch', 2)
        self.conveyor_barrier = \
            LightBarrier(self.rpi, 'conveyor barrier', 3)
        self.turntab_under_saw_switch = \
            ReferenceSwitch(self.rpi, 'turntable under saw switch', 4)
        self.vacuum_carrier_towards_turntable_switch = \
            ReferenceSwitch(self.rpi, 'vacuum carrier towards turntable switch', 5)
        self.inside_oven_switch = \
            ReferenceSwitch(self.rpi, 'inside oven switch', 6)
        self.outside_oven_switch = \
            ReferenceSwitch(self.rpi, 'outside oven switch', 7)
        self.vacuum_carrier_towards_oven_switch = \
            ReferenceSwitch(self.rpi, 'vacuum carrier towards oven switch', 8)
        self.oven_barrier = \
            LightBarrier(self.rpi, 'oven barrier', 9)
        
        # Prod positioning variables
        self.prod_on_oven_carrier = False
        self.prod_on_vacuum_carrier = False
        self.prod_on_oven_carrier = False
        self.prod_on_turntable = False
        self.prod_on_conveyor = False
        
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

        # Processes completed bool sensors
        self.bool_oven_proc_completed = False
        self.bool_vacuum_carrier_proc_completed = False
        self.bool_turntable_proc_completed = False
        self.bool_saw_proc_completed = False
        self.bool_conveyor_proc_completed = False

        # Sync sensors digital values with the values of the physical model
        #self.read()
        

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program
        print('Cleaning the system state')
        self.rpi.core.a1green.value = False
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
        # Prod positioning variables
        self.prod_on_oven_carrier = False
        self.prod_on_vacuum_carrier = False
        self.prod_on_oven_carrier = False
        self.prod_on_turntable = False
        self.prod_on_conveyor = False
        
        # Support time sensors
        self.time_sens_saw_count = 0
        self.time_sens_oven_count = 0
        self.time_sens_vacuum_count = 0
        self.time_sens_delivery_count = 0 
        self.time_sens_turntable_pusher_count = 0
        self.counter = 0

        # Processes completed bool sensors
        self.bool_oven_proc_completed = False
        self.bool_vacuum_carrier_proc_completed = False
        self.bool_turntable_proc_completed = False
        self.bool_saw_proc_completed = False
        self.bool_conveyor_proc_completed = False

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        # Activating the process services - i.e. the compressor
        #self.act_compressor = True
        self.compressor.turn_on()
        
        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 2 things, continuously: 
        #   1. Sets the Rpi a1 light
        #   2. Follows the process description
        while (self.rpi.exitsignal.wait(0.05) == False):
            # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
            # do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            # Follows the process description ###############################
            # If the oven-light sensor is False, that is there is the product
            # So, set the self.prod_on_oven_carrier to True
            if (self.oven_barrier.getState() == False):
                self.prod_on_oven_carrier = True
            
            # If there is the product on the oven carrier, move the vacuum 
            # carrier towards the oven
            if (self.bool_oven_proc_completed == False and 
                self.prod_on_oven_carrier == True):
                # Move the carrier towards the oven
                if (self.vacuum_carrier_towards_oven_switch.getState() == False):
                    # Activate it towards the oven
                    self.vacuum_carrier.move_towards_A()
                else:
                    # Deactivate it towards the oven
                    self.vacuum_carrier.turn_off()
                    
            # If the oven is not ready and the vacuum carrier grip is at the 
            # oven and the product is on the oven carrier: 
            if (self.bool_oven_proc_completed == False and
                self.prod_on_oven_carrier == True and 
                self.vacuum_carrier_towards_oven_switch.getState() == True):
                # Move inside the oven the oven carrier
                if (self.inside_oven_switch.getState() == False):
                    # TODO: FROM HERE WRAP INTO A SINGLE FUNCTION
                    # Open the door
                    self.oven_door_opening.turn_on()
                    # Move the feeder in the oven
                    self.oven_carrier.move_towards_A()
                # If the oven feeder is inside the oven
                else:
                    # Deactivate the inward oven
                    self.oven_carrier.turn_off()
                    # Close the door
                    self.oven_door_opening.turn_off()
                    # TODO: modify so that the light flashes only AFTER the door is completely closed
                    #haha, flashing lights go brrrr - For light flashing
                    if (self.time_sens_oven_count % 2 == 1):
                        # Activate the process light
                        self.oven_proc_light.turn_on()
                    else:
                        # Deactivate the process light
                        self.oven_proc_light.turn_off()
                    # Time counter
                    self.time_sens_oven_count += 1            

                # If the counter reaches 30, stop the oven process
                if (self.time_sens_oven_count >= 30):       
                    # Deactivate the light
                    self.oven_proc_light.turn_off()
                    # Set the oven process var to True
                    self.bool_oven_proc_completed = True
                    # Set the oven counter to 0
                    self.time_sens_oven_count = 0
            # If the oven is ready
            elif (self.bool_oven_proc_completed == True and 
                  self.prod_on_oven_carrier == True):
                # If oven_feeder_out sensor is False = the carrier is not 
                # out
                if (self.outside_oven_switch.getState() == False):
                    # Open the door
                    self.oven_door_opening.turn_on()
                    # Move the oven outside
                    self.oven_carrier.move_towards_B()
                else:
                    # Stop moving the oven carrier
                    self.oven_door_opening.turn_off()
                    # Close the door
                    self.oven_carrier.turn_off()
                        
            # Take the product with the carrier grip
            # Lower the vacuum gripper
            # If oven feeder sensor is True and oven ready is True and the
            # vacuum gripper variable is True and vacuum counter is less
            # than 10, that is if the oven feeder is out from the oven and
            # the oven is in ready state and the vacuum carrieer gripper 
            # is at the oven and the vacuum counter is less than 10
            # The counter is needed in order to wait for the vacuum gripper
            # to be completely lowered  
            if (self.outside_oven_switch.getState() == True 
                and self.bool_oven_proc_completed == True
                and self.vacuum_carrier_towards_oven_switch.getState() == True 
                and self.prod_on_oven_carrier == True):
                if (self.time_sens_vacuum_count < 10):
                    # Lower the carrier vacuum gripper
                    self.vacuum_grip_lowering.turn_on()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                # Grip the product 
                # If vacuum count is greater than 10 and less than 15
                if (self.time_sens_vacuum_count >= 10 and 
                    self.time_sens_vacuum_count < 15):
                    # Activate the carrier vacuum gripper
                    self.vacuum_valve_grip.turn_on()
                    # Add 1 to the vacuum count
                    self.time_sens_vacuum_count += 1

                # Raise the vacuum gripper 
                # If vacuum count is greater than 15 and less than 25
                if (self.time_sens_vacuum_count >= 15 and 
                        self.time_sens_vacuum_count < 25):
                    # Upper the carrier vacuum gripper
                    self.vacuum_grip_lowering.turn_off()
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                if(self.vacuum_carrier_towards_oven_switch.getState() == True
                    and self.vacuum_grip_lowering.getState() == False
                    and self.vacuum_valve_grip.getState() == True
                    and self.time_sens_vacuum_count >= 25):
                    self.time_sens_vacuum_count = 0
                    self.prod_on_oven_carrier = False
                    self.prod_on_vacuum_carrier = True
            
            # Move the carrier to the turnta#ble
            if (self.prod_on_vacuum_carrier == True and 
                self.vacuum_carrier_towards_turntable_switch.getState() == False):
                # Bring the carrier vacuum gripper to the turn-table
                self.vacuum_carrier.move_towards_B()
            elif (self.prod_on_vacuum_carrier == True and 
                self.vacuum_carrier_towards_turntable_switch.getState() == True):
                # Stop the vacuum carrier
                self.vacuum_carrier.turn_off()
            
            # Release the product
            # Lower the carrier vacuum gripper
            if (self.vacuum_carrier_towards_turntable_switch.getState() == True 
                and self.prod_on_vacuum_carrier == True
                and self.vacuum_valve_grip.getState() == True
                and self.time_sens_vacuum_count < 15):
                    self.vacuum_grip_lowering.turn_on()
                    self.time_sens_vacuum_count += 1
            # Release the product on the turntable
            elif (self.vacuum_carrier_towards_turntable_switch.getState() == True 
                and self.vacuum_grip_lowering.getState() == True
                and self.time_sens_vacuum_count >= 15 
                and self.time_sens_vacuum_count < 30):
                    self.vacuum_valve_grip.turn_off()
                    self.time_sens_vacuum_count += 1
            # Raise the carrier vacuum gripper
            elif (self.vacuum_carrier_towards_turntable_switch.getState() == True 
                and self.vacuum_grip_lowering.getState() == True
                and self.vacuum_valve_grip.getState() == False
                and self.time_sens_vacuum_count >= 30):
                    self.time_sens_vacuum_count = 0
                    self.vacuum_grip_lowering.turn_off()
                    self.prod_on_vacuum_carrier = False
                    self.bool_vacuum_carrier_proc_completed = True
                    self.prod_on_turntable = True

            # Turn the turntable towards the saw
            if (self.prod_on_turntable == True and
                self.bool_turntable_proc_completed == False):
                # Activate the turntable until it reaches the saw
                if (self.turntab_under_saw_switch.getState() == False and
                    self.bool_saw_proc_completed == False):
                    self.turntable.move_towards_A()
                elif(self.turntab_under_saw_switch.getState() == True and
                    self.bool_saw_proc_completed == False):
                    self.turntable.turn_off()

                # Activate the saw for the design processing time
                if (self.turntab_under_saw_switch.getState() == True and 
                    self.bool_saw_proc_completed == False and
                    self.time_sens_saw_count < 40):
                    self.saw.turn_on()
                    self.time_sens_saw_count += 1
                elif (self.turntab_under_saw_switch.getState() == True and 
                    self.time_sens_saw_count >= 40): 
                    self.saw.turn_off()
                    self.bool_saw_proc_completed = True
                    self.time_sens_saw_count = 0
            
                # Activate the turntable until it reaches the conveyor                
                if (self.bool_saw_proc_completed == True and
                    self.turntab_towards_conveyor_switch.getState() == False):
                    self.turntable.move_towards_A()
                elif (self.bool_saw_proc_completed == True and
                    self.turntab_towards_conveyor_switch.getState() == True): 
                    self.turntable.turn_off()
            
                # Activate the pusher
                if (self.turntab_towards_conveyor_switch.getState() == True and
                    self.time_sens_turntable_pusher_count < 20):
                    self.turntable_pusher.turn_on()
                    self.time_sens_turntable_pusher_count += 1
                elif(self.turntab_towards_conveyor_switch.getState() == True and
                    self.time_sens_turntable_pusher_count >= 20):
                    self.turntable_pusher.turn_off()
                    self.prod_on_turntable = False
                    self.prod_on_conveyor = True
                    self.time_sens_turntable_pusher_count = 0
            
            # Activate the conveyor
            if (self.prod_on_conveyor == True):
                if (self.conveyor_barrier.getState() == True):
                    self.conveyor.turn_on()
                elif (self.conveyor_barrier.getState() == False): 
                    self.conveyor.turn_off()

            #################################################################
            # Otherwise, if there is the product in front of the light sensor
            if(self.conveyor_barrier.getState() == False):
                # Turn off the services
                self.compressor.turn_off()
                
                # Turn off the valve feeder
                self.turntable_pusher.turn_off()

                # Turn off the conveyor belt
                self.conveyor.turn_off()
                
                # Turn the turn-table towards the carrier
                # If the turntable_pos_vacuum sensor is False, that is 
                # if the turntable is not at the vacuum gripper carrier
                if (self.turntab_under_vacuum_switch.getState() == False):
                    # Activate the conveyor rotation clockwise
                    self.turntable.move_towards_B()
                # Otherwise, if the turntable_pos_vacuum sensor is True, that 
                # is if the turntable is at the vacuum gripper carrier
                else:
                    # Deactivate the conveyor rotation clockwise
                    self.turntable.turn_off()

                # Finally, reset the counters
                self.reset_station_states()


if __name__ == "__main__":
    # Instantiating the controlling class
    root = CycleEventManager()
    # Launch the start function of the RevPi event control system
    root.start()
