#!/usr/bin/env python

"""
cycle_event_manager.py: CycleEventManagerRevPi class

This class is aimed at controlling the whole Fischertechnik loop process. 
The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
from machine_group import MachineGroup
from time import sleep

class CycleEventManager():
    """Entry point for Fischertechnik Multiprocess Station with Oven control 
    over RevPi."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)
        #create multiprocessing object (not the Python Multiprocessing lib!)
        #self.machine_group = MachineGroup(1)
        self.machine_group = MachineGroup()


    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False
        self.rpi.io['O_1'].value = False
        self.rpi.io['O_2'].value = False
        self.rpi.io['O_3'].value = False
        self.rpi.io['O_4'].value = False
        self.rpi.io['O_5'].value = False
        self.rpi.io['O_6'].value = False
        self.rpi.io['O_7'].value = False
        self.rpi.io['O_8'].value = False

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)
        # My own loop to do some work next to the event system. We will stay
        # here till self.rpi.exitsignal.wait returns True after SIGINT/SIGTERM
        # The loop does 3 things, continuously: 
        #   0. Sets the Rpi a1 light
        #   1. Reads the sensors states
        #   2. Calls the .process_product function
        #   3. Writes the actuators desired states
        while not self.rpi.exitsignal.wait(0.05):
            # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
            # do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value
            
            # 1. Reads the sensors states
            self.read()

            # 2. Calls the machine_group.process_product process description
            self.machine_group.process_product()
            
            # 3. Writes the actuators desired states
            self.write()

    def read(self):
        """Reads the input sensors states"""
        # Assigning to a the relative variable, the sensor value
        # Reference switch - Turntable under vacuum carrier
        self.machine_group.turntable_pos_vacuum = self.rpi.io['I_1'].value
        # Reference switch - Turntable aligned to position conveyor
        self.machine_group.turntable_pos_conveyor = self.rpi.io['I_2'].value
        # Light sensor - Conveyor belt
        self.machine_group.sens_delivery= self.rpi.io['I_3'].value
        # Reference switch - Turn-table under saw
        self.machine_group.turntable_pos_saw  = self.rpi.io['I_4'].value
        # Reference switch - Vacuum carrier aligned to turn-table
        self.machine_group.vacuum_gripper_at_turntable = self.rpi.io['I_5'].value
        # Reference switch - Oven carrier inside the oven
        self.machine_group.oven_feeder_in = self.rpi.io['I_6'].value
        # Reference switch - Oven carrier outside the oven
        self.machine_group.oven_feeder_out  = self.rpi.io['I_7'].value
        # Reference switch - Vacuum carrier aligned to oven
        self.machine_group.vacuum_gripper_at_oven = self.rpi.io['I_8'].value
        # Light sensor - Oven
        self.machine_group.sens_oven = self.rpi.io['I_9'].value

    def write(self):
        """Writes the output actuators states"""
        # Assigning to a the relative sensor, the variable value
        # Turn-table - Motor clock wise        
        self.rpi.io['O_1'].value = self.machine_group.act_rot_clockwise
        # Turn-table - Motor counter-clock wise
        self.rpi.io['O_2'].value = self.machine_group.act_rot_counterclockwise
        # Conveyor belt - Motor forward
        self.rpi.io['O_3'].value = self.machine_group.act_conveyor_forward
        # Saw - Motor activation
        self.rpi.io['O_4'].value = self.machine_group.act_saw
        # Oven - Carrier oven motor move inside
        self.rpi.io['O_5'].value = self.machine_group.act_oven_inward
        # Oven - Carrier oven motor move outside
        self.rpi.io['O_6'].value = self.machine_group.act_oven_outward
        # Vacuum carrier - Motor move towards oven
        self.rpi.io['O_7'].value = self.machine_group.act_gripper_to_oven
        # Vacuum carrier - Move towards turn-table
        self.rpi.io['O_8'].value = self.machine_group.act_gripper_to_turntable
        # Oven - Processing light
        self.rpi.io['O_9'].value = self.machine_group.oven_light
        # Compressor - activation
        self.rpi.io['O_10'].value = self.machine_group.compressor
        # Vacuum carrier - Vacuum valve grip activation
        self.rpi.io['O_11'].value = self.machine_group.valve
        # Vacuum carrier - Vacuum valve lowering activation
        self.rpi.io['O_12'].value = self.machine_group.act_lower_valve
        # Oven - Door opening activation
        self.rpi.io['O_13'].value = self.machine_group.valve_oven_door
        # Turn-table - Pusher valve activation
        self.rpi.io['O_14'].value = self.machine_group.valve_feeder


if __name__ == "__main__":
    # Instantiating the controlling class
    root = CycleEventManager()
    # Launch the start function of the RevPi event control system
    root.start()
