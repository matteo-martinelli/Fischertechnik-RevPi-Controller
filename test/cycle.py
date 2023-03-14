#!/usr/bin/env python

"""
cycle_event_manager.py: CycleEventManagerRevPi class

This class is aimed at controlling the whole Fischertechnik loop process. 
The loop is managed via the RevPi event manager, that is set for being not 
blocking, with a personalised while loop next to the event system. 
"""


import revpimodio2
from test_actuator import TestActuator

class TestCycle():
    """Testing over the RevPi OOP functionalities."""
    def __init__(self):
        # Instantiate RevPiModIO controlling library
        self.rpi = revpimodio2.RevPiModIO(autorefresh=True)
        # Handle SIGINT / SIGTERM to exit program cleanly
        self.rpi.handlesignalend(self.cleanup_revpi)

        # Instantiating all the needed objects
        self.my_actuator = TestActuator(self.rpi)
        

    def cleanup_revpi(self):
        """Cleanup function to leave the RevPi in a defined state."""
        # Switch of LED and outputs before exit program
        self.rpi.core.a1green.value = False

    def start(self):
        """Start event system and own cyclic loop."""
        print('start')
        # Start event system loop without blocking here. Reference at 
        # https://revpimodio.org/en/events-in-the-mainloop/
        self.rpi.mainloop(blocking=False)

        self.rpi.core.a1green.value = True

        while (self.rpi.exitsignal.wait(0.05) == False):
            # Sets the Rpi a1 light: switch on / off green part of LED A1 | or 
            # do other things
            
            self.my_actuator.cycle_test()

if __name__ == "__main__":
    # Instantiating the controlling class
    root = TestCycle()
    # Launch the start function of the RevPi event control system
    root.start()
