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


class MotorRetarderSystemAnomaly(object):
    """Conveyor Carrier class for conveyor objects."""
    def __init__(self, name: str, motor: [RevPiSingleMotionActuator, 
                                          RevPiDoubleMotionActuator]):
        self.logger = logging.getLogger('multiproc_dept_logger')
        self._name = name
        self._motor_to_retard = motor
        self.restarted_thread_on = False


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
            self.__stopping_motor(4)
             # TODO: maybe could be better to divide into 3 steps: stop, wait, restart, an implement the associated functions.
            self.__restarting_motor(pin)
            time.sleep(2)
            self.restarted_thread_on = False
        elif (speed_level == "Medium"):
            self.__stopping_motor(2)
            self.__restarting_motor(pin)
            time.sleep(2)
            self.restarted_thread_on = False
        elif (speed_level == "High"):
            #self.logger.info('No stop planned')
            pass
        else: 
            self.logger.error('Illegal conveyor speed configuration ' +
                            ' received in transfering product to the exit;' + 
                            ' expected \"Low\" or \"Medium\" or' +
                            ' \"High\", got %s', speed_level)

    def __stopping_motor(self, stopping_time: [int, float] = -1) -> None: 
        if (time != -1):
            self.motor_to_retard.turn_off()
            self.logger.info('Stopping for {} seconds'.format(stopping_time))
            # Alternative to time.sleep(5)
            time_sleep = threading.Thread(name=self._name, 
                                        target=time.sleep, 
                                        args=(stopping_time,)) 
            time_sleep.start()
            time_sleep.join()
            self.logger.info('Stopped for {} seconds'.format(stopping_time))
        else: 
            self.logger.error('Wrong input time given, expected a positive ' + 
                              'int or float number, got {}'
                              .format(stopping_time))

    def __restarting_motor(self, pin: int = -1) -> None: 
        motor_type_single_actuator = \
            "<class 'components." + \
                "revpi_single_motion_actuator.RevPiSingleMotionActuator'>"
        motor_type_double_actuator = \
            "<class 'components." + \
                "revpi_double_motion_actuator.RevPiDoubleMotionActuator'>"
        if (str(type(self.motor_to_retard)) == motor_type_single_actuator): 
            self.motor_to_retard.turn_on()
        elif (str(type(self.motor_to_retard)) == motor_type_double_actuator): 
            if(pin == -1):
                self.logger.error('Wrong input time given to double motion ' + 
                                  'actuator restarter, expected a ' + 
                                  'positive int number, got {}'.format(pin))
            else: 
                self.motor_to_retard.turn_on(self.motor_to_retard\
                                             ._pin_tuple[pin])
        else: 
            self.logger.error('Wrong motor type passed, expected a ' + 
                              'SingleMotionActuator or a ' + 
                              'DoubleMotionActuator, got {}'
                              .format(str(type(self.motor_to_retard))))