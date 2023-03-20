#!/usr/bin/env python

"""
vacuum_actuator.py: VacuumActuator class

For following pins: 
O_11: vacuum gripper on carrier activation;
O_12: vacuum gripper on carrier lowering;
O_13: vacuum activated oven doors opening;
O_14: turntable vacuum pusher activation.
"""

from components.single_motion_actuator import SingleMotionActuator


class VacuumActuator(SingleMotionActuator):
    """Vacuum Actuator class for vacuum activated objects."""
    def __init__(self, rpi, name: str, pin: int):
        super().__init__(rpi, pin)
        self.name = name


    def getName(self) -> str:
        return self.name
