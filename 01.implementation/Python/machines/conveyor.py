#!/usr/bin/env python

"""
conveyor_carrier.py: Conveyor class

This class is composed by the following objects: 
    1. single activation motor O_3; 
    2. light barrier sensor I_3;
"""

from components.revpi_single_motion_actuator import RevPiSingleMotionActuator
from components.revpi_light_barrier import RevPiLightBarrier
import datetime


class Conveyor(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, rpi, mqtt_publisher):
        # Class actuators
        self.motor = \
            RevPiSingleMotionActuator(rpi, 'conveyor-motor', 3)
        # Class sensors
        self.light_barrier = \
            RevPiLightBarrier(rpi, 'conveyor-light-barrier', 3)
        # Class virtual sensors
        self.prod_on_conveyor = False
        self.process_completed = False
        # MQTT 
        #self.name = pass
        #self.dept = pass # TODO: will represent the main topic
        self.mqtt_publisher = mqtt_publisher
        self.topic = 'services/compressor/telemetry'


    def move_to_the_exit(self) -> None:
        while (self.light_barrier.get_state() != False):
            self.motor.turn_on()
        self.motor.turn_off()

    def to_dto(self):
        current_moment = datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

        dto_dict = {
            'name': self.name,
            'pin': self.pin,
            'state': self.state,
            'timestamp': current_moment 
        }
        return dto_dict
