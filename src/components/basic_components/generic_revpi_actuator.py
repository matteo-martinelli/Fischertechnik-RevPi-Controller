#!/usr/bin/env python

"""
generic_actuator.py: GenericActuator class

This is the root class for every actuator used in the simulation. 
It collects all the common fields and methods of any simulation actuator.  
"""


import revpimodio2


class GenericRevPiActuator(object):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi: revpimodio2.RevPiModIO):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        self._state = False
        self._previous_state = False
