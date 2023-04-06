#!/usr/bin/env python

"""
generic_actuator.py: GenericActuator class

This is the root class for every actuator used in the simulation. 
It collects all the common fields and methods of any simulation actuator.  
"""


class GenericRevPiActuator(object):
    """Reference Switch class for reference switch objects."""
    def __init__(self, rpi):
        # Instantiate RevPiModIO controlling library
        self.rpi = rpi
        # TODO: eventually assign directly here the state from revpimodio
        self.state = False
        self.previous_state = False
