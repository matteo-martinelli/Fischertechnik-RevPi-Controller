#!/usr/bin/env python

"""
cycle_event_manager.py: CycleEventManagerRevPi class

This class is aimed at controlling the whole Fischertechnik loop process. 
The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
import time
from saw import Saw

class TestCycle():
    """Testing over the RevPi OOP functionalities."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)
        
        # Saw process time counter
        self.time_sens_saw_count = 0

        # Instantiating all the needed objects
        self.saw = Saw()
        

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False
        # Support time sensors
        self.time_sens_saw_count = 0
    
    def write(self):
        """Writes the output actuators states"""
        # Assigning to a the relative sensor, the variable value
        # Saw - Motor activation
        #self.rpi.io['O_4'].value = self.act_saw
        

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        while (self.rpi.exitsignal.wait(0.05) == False):
            # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
            # do other things
            self.rpi.core.a1green.value = not self.rpi.core.a1green.value

            # 2. Makes something
            if (self.time_sens_saw_count < 30):
                self.saw.turn_on()
            else:
                self.saw.turn_off()
                self.time_sens_saw_count = 0
                time.sleep(5)
                

if __name__ == "__main__":
    # Instantiating the controlling class
    root = TestCycle()
    # Launch the start function of the RevPi event control system
    root.start()
