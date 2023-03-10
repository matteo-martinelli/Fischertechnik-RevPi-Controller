#!/usr/bin/env python

"""
cycle_event_manager.py: CycleEventManagerRevPi class

This class is aimed at controlling the whole Fischertechnik loop process. 
The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
#from oven import Oven

class CycleEventManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)
        
        # Defining actuators class variables
        # Turn-table - Motor clock wise        
        self.act_turntable_clockwise = False
        # Turn-table - Motor counter-clock wise
        self.act_turntable_counterclockwise = False
        # Conveyor belt - Motor forward
        self.act_conveyor = False
        # Saw - Motor activation
        self.act_saw = False
        # Oven - Carrier oven motor move inside
        self.act_oven_career_inward = False
        # Oven - Carrier oven motor move outside
        self.act_oven_career_outward = False
        # Vacuum carrier - Motor move towards oven
        self.act_vacuum_carrier_to_oven = False
        # Vacuum carrier - Move towards turn-table
        self.act_vacuum_carrier_to_turntable = False
        # Oven - Processing light
        self.act_oven_process_light = False
        # Compressor - activation
        self.act_compressor = False
        # Vacuum carrier - Vacuum valve grip activation
        self.act_carrier_vacuum_gripper = False
        # Vacuum carrier - Vacuum valve lowering activation
        self.act_carrier_vacuum_gripper_lowering = False
        # Oven - Door opening activation
        self.act_vacuum_oven_door = False
        # Turn-table - Pusher valve activation
        self.act_turntable_vacuum_pusher = False

        # Defining sensor class varaibles
        # Reference switch - Turntable under vacuum carrier
        self.sens_turntable_towards_vacuum_ref_switch = False
        # Reference switch - Turntable aligned to position conveyor
        self.sens_turntable_towards_conveyor_ref_switch = False
        # Light sensor - Conveyor belt
        self.sens_conveyor_light_barrier = False
        # Reference switch - Turn-table under saw
        self.sens_turntable_towards_saw_ref_switch = False
        # Reference switch - Vacuum carrier aligned to turn-table
        self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch = False
        # Reference switch - Oven carrier inside the oven
        self.sens_oven_carrier_in_ref_switch = False
        # Reference switch - Oven carrier outside the oven
        self.sens_oven_carrier_out_ref_switch = False
        # Reference switch - Vacuum carrier aligned to oven
        self.sens_vacuum_gripper_carrier_towards_oven_ref_switch = False
        # Light sensor - Oven
        self.sens_oven_light_barrier = False
        
        # Prod positioning variables
        self.prod_on_oven_carrier = False
        self.prod_on_vacuum_carrier = False
        self.prod_on_oven_carrier = False
        self.prod_on_turntable = False
        self.prod_on_conveyor = False
        
        # Support time sensors # TODO: evaluate if is worth to use all those vars or only one is enough
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
        self.read()
        

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


    def read(self):
        """Reads the input sensors states"""
        # Assigning to a the relative variable, the sensor value
        # Reference switch - Turntable under vacuum carrier
        self.sens_turntable_towards_vacuum_ref_switch = \
            self.rpi.io['I_1'].value
        # Reference switch - Turntable aligned to position conveyor
        self.sens_turntable_towards_conveyor_ref_switch = \
            self.rpi.io['I_2'].value
        # Light sensor - Conveyor belt
        self.sens_conveyor_light_barrier = \
            self.rpi.io['I_3'].value
        # Reference switch - Turn-table under saw
        self.sens_turntable_towards_saw_ref_switch = \
            self.rpi.io['I_4'].value
        # Reference switch - Vacuum carrier aligned to turn-table
        self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch = \
            self.rpi.io['I_5'].value
        # Reference switch - Oven carrier inside the oven
        self.sens_oven_carrier_in_ref_switch = \
            self.rpi.io['I_6'].value
        # Reference switch - Oven carrier outside the oven
        self.sens_oven_carrier_out_ref_switch = \
            self.rpi.io['I_7'].value
        # Reference switch - Vacuum carrier aligned to oven
        self.sens_vacuum_gripper_carrier_towards_oven_ref_switch = \
            self.rpi.io['I_8'].value
        # Light sensor - Oven
        self.sens_oven_light_barrier = \
            self.rpi.io['I_9'].value
    
    def write(self):
        """Writes the output actuators states"""
        # Assigning to a the relative sensor, the variable value
        # Turn-table - Motor clock wise        
        self.rpi.io['O_1'].value = self.act_turntable_clockwise
        # Turn-table - Motor counter-clock wise
        self.rpi.io['O_2'].value = self.act_turntable_counterclockwise
        # Conveyor belt - Motor forward
        self.rpi.io['O_3'].value = self.act_conveyor
        # Saw - Motor activation
        self.rpi.io['O_4'].value = self.act_saw
        # Oven - Carrier oven motor move inside
        self.rpi.io['O_5'].value = self.act_oven_career_inward
        # Oven - Carrier oven motor move outside
        self.rpi.io['O_6'].value = self.act_oven_career_outward
        # Vacuum carrier - Motor move towards oven
        self.rpi.io['O_7'].value = self.act_vacuum_carrier_to_oven
        # Vacuum carrier - Move towards turn-table
        self.rpi.io['O_8'].value = self.act_vacuum_carrier_to_turntable
        # Oven - Processing light
        self.rpi.io['O_9'].value = self.act_oven_process_light
        # Compressor - activation
        self.rpi.io['O_10'].value = self.act_compressor
        # Vacuum carrier - Vacuum valve grip activation
        self.rpi.io['O_11'].value = self.act_carrier_vacuum_gripper
        # Vacuum carrier - Vacuum valve lowering activation
        self.rpi.io['O_12'].value = self.act_carrier_vacuum_gripper_lowering
        # Oven - Door opening activation
        self.rpi.io['O_13'].value = self.act_vacuum_oven_door
        # Turn-table - Pusher valve activation
        self.rpi.io['O_14'].value = self.act_turntable_vacuum_pusher

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        # Instantiating all the needed objects
        #oven = Oven

        # Activating the process services - i.e. the compressor
        self.act_compressor = True

        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 3 things, continuously: 
        #   0. Sets the Rpi a1 light
        #   1. Reads the sensors states
        #   2. Calls the .process_product function
        #   3. Writes the actuators desired states
        while (self.rpi.exitsignal.wait(0.05) == False):
            # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
            # do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            # 1. Reads the sensors states
            self.read()

            # 2. Calls the machine_group.process_product process description
            # If the oven-light sensor is False, that is there is the product
            # So, set the self.prod_on_oven_carrier to True
            if (self.sens_oven_light_barrier == False):
                # If oven_ready == False
                self.prod_on_oven_carrier = True
            
            # If there is the product on the oven carrier, move the vacuum 
            # carrier towards the oven
            if (self.bool_oven_proc_completed == False and 
                self.prod_on_oven_carrier == True):
                # Move the carrier towards the oven
                if (self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == False):
                    # Activate it towards the oven
                    self.act_vacuum_carrier_to_oven = True
                else:
                    # Deactivate it towards the oven
                    self.act_vacuum_carrier_to_oven = False
                    
            # If the oven is not ready and the vacuum carrier grip is at the oven
            # and the product is on the oven carrier: 
            if (self.bool_oven_proc_completed == False and
                self.prod_on_oven_carrier == True and 
                self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == True):
                # Move inside the oven the oven carrier
                if (self.sens_oven_carrier_in_ref_switch == False):
                    # TODO: FROM HERE WRAP INTO A SINGLE FUNCTION
                    # Open the door
                    self.act_vacuum_oven_door = True
                    #oven.door_open
                    # Move the feeder in the oven
                    self.act_oven_career_inward = True
                # If the oven feeder is inside the oven
                else:
                    # Deactivate the inward oven
                    self.act_oven_career_inward = False
                    # Close the door
                    self.act_vacuum_oven_door = False
                    #oven.door_close
                    # TODO: modify so that the light flashes only AFTER the door is completely closed
                    #haha, flashing lights go brrrr - For light flashing
                    if (self.time_sens_oven_count % 2 == 1):
                        # Activate the process light
                        self.act_oven_process_light = True
                    else:
                        # Deactivate the process light
                        self.act_oven_process_light = False
                    # Time counter
                    self.time_sens_oven_count += 1            

                # If the counter reaches 30, stop the oven process
                if (self.time_sens_oven_count >= 30):       
                    # Deactivate the light
                    self.act_oven_process_light = False
                    # Set the oven process var to True
                    self.bool_oven_proc_completed = True
                    # Set the oven counter to 0
                    self.time_sens_oven_count = 0
            # If the oven is ready
            elif (self.bool_oven_proc_completed == True and 
                  self.prod_on_oven_carrier == True):
                # TODO: FROM HERE WRAP INTO A SINGLE FUNCTION
                #self.move_feeder_out() function
                # If oven_feeder_out sensor is False = the carrier is not 
                # out
                if (self.sens_oven_carrier_out_ref_switch == False):
                    # Open the door
                    self.act_vacuum_oven_door = True
                    # Move the oven outside
                    self.act_oven_career_outward = True
                else:
                    # Stop moving the oven carrier
                    self.act_oven_career_outward = False
                    # Close the door
                    self.act_vacuum_oven_door = False
                        
            # Take the product with the carrier grip
            # Lower the vacuum gripper
            # If oven feeder sensor is True and oven ready is True and the
            # vacuum gripper variable is True and vacuum counter is less
            # than 10, that is if the oven feeder is out from the oven and
            # the oven is in ready state and the vacuum carrieer gripper 
            # is at the oven and the vacuum counter is less than 10
            # The counter is needed in order to wait for the vacuum gripper
            # to be completely lowered  
            if (self.sens_oven_carrier_out_ref_switch == True 
                and self.bool_oven_proc_completed == True
                and self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == True 
                and self.prod_on_oven_carrier == True):
                if (self.time_sens_vacuum_count < 10):
                    # Lower the carrier vacuum gripper
                    self.act_carrier_vacuum_gripper_lowering = True
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                # Grip the product 
                # If vacuum count is greater than 10 and less than 15
                if (self.time_sens_vacuum_count >= 10 and 
                    self.time_sens_vacuum_count < 15):
                    # Activate the carrier vacuum gripper
                    self.act_carrier_vacuum_gripper = True 
                    # Add 1 to the vacuum count
                    self.time_sens_vacuum_count += 1

                # Raise the vacuum gripper 
                # If vacuum count is greater than 15 and less than 25
                if (self.time_sens_vacuum_count >= 15 and 
                        self.time_sens_vacuum_count < 25):
                    # Upper the carrier vacuum gripper
                    self.act_carrier_vacuum_gripper_lowering = False
                    # Add 1 to the vacuum counter
                    self.time_sens_vacuum_count += 1
            
                if(self.sens_vacuum_gripper_carrier_towards_oven_ref_switch == True
                    and self.act_carrier_vacuum_gripper_lowering == False
                    and self.act_carrier_vacuum_gripper == True
                    and self.time_sens_vacuum_count >= 25):
                    self.time_sens_vacuum_count = 0
                    self.prod_on_oven_carrier = False
                    self.prod_on_vacuum_carrier = True
            
            # Move the carrier to the turntable
            if (self.prod_on_vacuum_carrier == True and 
                self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == False):
                # Bring the carrier vacuum gripper to the turn-table
                self.act_vacuum_carrier_to_turntable = True
            elif (self.prod_on_vacuum_carrier == True and 
                self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True):
                self.act_vacuum_carrier_to_turntable = False
            
            # Release the product
            # Lower the carrier vacuum gripper
            if (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True 
                and self.prod_on_vacuum_carrier == True
                and self.act_carrier_vacuum_gripper == True
                and self.time_sens_vacuum_count < 15):
                    self.act_carrier_vacuum_gripper_lowering = True
                    self.time_sens_vacuum_count += 1
            # Release the product on the turntable
            elif (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True 
                and self.act_carrier_vacuum_gripper_lowering == True
                and self.time_sens_vacuum_count >= 15 
                and self.time_sens_vacuum_count < 30):
                    self.act_carrier_vacuum_gripper = False
                    self.time_sens_vacuum_count += 1
            # Raise the carrier vacuum gripper
            elif (self.sens_vacuum_gripper_carrier_towards_turntable_ref_switch == True 
                and self.act_carrier_vacuum_gripper_lowering == True
                and self.act_carrier_vacuum_gripper == False
                and self.time_sens_vacuum_count >= 30):
                    self.time_sens_vacuum_count = 0
                    self.act_carrier_vacuum_gripper_lowering = False
                    self.prod_on_vacuum_carrier = False
                    self.bool_vacuum_carrier_proc_completed = True
                    self.prod_on_turntable = True

            # Turn the turntable towards the saw
            if (self.prod_on_turntable == True and
                self.bool_turntable_proc_completed == False):
                # Activate the turntable until it reaches the saw
                if (self.sens_turntable_towards_saw_ref_switch == False and
                    self.bool_saw_proc_completed == False):
                    self.act_turntable_clockwise = True
                elif(self.sens_turntable_towards_saw_ref_switch == True and
                    self.bool_saw_proc_completed == False):
                    self.act_turntable_clockwise = False
            
                # Activate the saw for the design processing time
                if (self.sens_turntable_towards_saw_ref_switch == True and 
                    self.bool_saw_proc_completed == False and
                    self.time_sens_saw_count < 40):
                    self.act_saw = True
                    self.time_sens_saw_count += 1
                elif (self.sens_turntable_towards_saw_ref_switch == True and 
                    self.time_sens_saw_count >= 40): 
                    self.act_saw = False
                    self.bool_saw_proc_completed = True
                    self.time_sens_saw_count = 0
            
                # Activate the turntable until it reaches the conveyor                
                if (self.bool_saw_proc_completed == True and
                    self.sens_turntable_towards_conveyor_ref_switch == False):
                    self.act_turntable_clockwise = True
                elif (self.bool_saw_proc_completed == True and
                    self.sens_turntable_towards_conveyor_ref_switch == True): 
                    self.act_turntable_clockwise = False
            
                # Activate the pusher
                if (self.sens_turntable_towards_conveyor_ref_switch == True and
                    self.time_sens_turntable_pusher_count < 20):
                    self.act_turntable_vacuum_pusher = True
                    self.time_sens_turntable_pusher_count += 1
                elif(self.sens_turntable_towards_conveyor_ref_switch == True and
                    self.time_sens_turntable_pusher_count >= 20):
                    self.act_turntable_vacuum_pusher = False
                    self.prod_on_turntable = False
                    self.prod_on_conveyor = True
                    self.time_sens_turntable_pusher_count = 0
            
            # Activate the conveyor
            if (self.prod_on_conveyor == True):
                print('on conv')
                if (self.sens_conveyor_light_barrier == True):
                    self.act_conveyor = True
                elif (self.sens_conveyor_light_barrier == False): 
                    self.act_conveyor = False

###############################################################################

            # Otherwise, if there is the product in front of the light sensor
            if(self.sens_conveyor_light_barrier == False):    
                # Turn off the services
                self.act_compressor = False
                
                # Turn off the valve feeder
                self.act_turntable_vacuum_pusher = False
                
                # Turn off the conveyor belt
                self.act_conveyor = False
                
                # Turn the turn-table towards the carrier
                #self.turntable_to_vacuum() function
                # If the turntable_pos_vacuum sensor is False, that is 
                # if the turntable is not at the vacuum gripper carrier
                if (self.sens_turntable_towards_vacuum_ref_switch == False):
                    # Activate the conveyor rotation clockwise
                    self.act_turntable_counterclockwise = True
                # Otherwise, if the turntable_pos_vacuum sensor is True, that 
                # is if the turntable is at the vacuum gripper carrier
                else:
                    # Deactivate the conveyor rotation clockwise
                    self.act_turntable_counterclockwise = False

                # Finally, reset the counters
                self.reset_station_states()    

            # 3. Writes the actuators desired states
            self.write()


if __name__ == "__main__":
    # Instantiating the controlling class
    root = CycleEventManager()
    # Launch the start function of the RevPi event control system
    root.start()
