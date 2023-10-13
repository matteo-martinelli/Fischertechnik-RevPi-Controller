#!/usr/bin/env python

"""
motor_retarder_system.py: MotorRetarderSystem class

Package of methods that allows the creation of an object whose responsibility 
is to stop and restart the passed motor for the correct amount of time.
"""


from ctypes import Union
import logging
import threading
import time

from components.revpi_double_motion_actuator import RevPiDoubleMotionActuator
from components.revpi_single_motion_actuator import RevPiSingleMotionActuator


class MotorRetarderSystem(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, name: str, motor: [RevPiSingleMotionActuator, 
                                          RevPiDoubleMotionActuator]):
        self.logger = logging.getLogger('multiproc_dept_logger')
        self._name = name
        self._motor_to_retard = motor


    # Getters
    @property
    def name(self) -> str: 
        return self._name

    @property
    def motor_to_retard(self) -> [RevPiSingleMotionActuator, 
                                  RevPiDoubleMotionActuator]: 
        return self._motor_to_retard

    # Class methods
    def stop_and_restart_motor(self, speed_level: str, pin: int = -1):
        if (speed_level == "Low"):
            self.__stoppping_motor(5)
            self.__restarting_motor(pin)
        elif (speed_level == "Medium"):
            self.__stoppping_motor(3)
            self.__restarting_motor(pin)
        elif (speed_level == "High"):
            self.logger.info('No stop planned')
        else: 
            self.logger.error('Illegal conveyor speed configuration ' +
                            ' received in transfering product to the exit;' + 
                            ' expected \"Low\" or \"Medium\" or' +
                            ' \"High\", got %s', speed_level)

    def __stoppping_motor(self, time: [int, float] = -1) -> None: 
        if (time != -1):
            self.motor_to_retard.turn_off()
            self.logger.info('Stopping for ' + time  + ' seconds')
            # Alternative to time.sleep(5)
            time_sleep = threading.Thread(name=self._name, 
                                        target=time.sleep, args=(time,)) 
            time_sleep.start()
            time_sleep.join()
            self.logger.info('Stopped for ' + time  + ' seconds')
        else: 
            self.logger.error('Wrong input time given, expecteda positive ' + 
                              'int or float number, got {}'.format(time))

    def __restarting_motor(self, pin: int = -1) -> None: 
        if (type(self.motor_to_retard) == "RevPiSingleMotionActuator"): 
            self.motor_to_retard.turn_on()
        else: 
            if(pin == -1):
                self.logger.error('Wrong input time given, expecteda ' + 
                                  'positive int number, got {}'.format(time))
            else: 
                self.motor_to_retard.turn_on(self.motor_to_retard\
                                             ._pin_tuple[pin])