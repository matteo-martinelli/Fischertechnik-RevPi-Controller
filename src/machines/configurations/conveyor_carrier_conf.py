#!/usr/bin/env python

"""
conveyor_carrier_conf.py: ConveyorCarrierConf class

Contains and represents the conveyor carrier configuration
"""

import logging


class ConveyorCarrierConf(object):
    def __init__(self, conveyor_carrier_speed: str) -> None:
        self._conveyor_carrier_speed = conveyor_carrier_speed
        self.logger = logging.getLogger('multiproc_dept_logger')
        
    @property
    def conveyor_carrier_speed(self) -> str: 
        return self._conveyor_carrier_speed
    
    @conveyor_carrier_speed.setter
    def conveyor_carrier_speed(self, value: str) -> None: 
        if(value == "Low" or value == "Medium" or value == "High"):
            self._conveyor_carrier_speed = value
        else: 
            self.logger.error('Illegal value passed to the conveyor ' +
                              'configuration. Expected \"High\", \"Medium\" ' + 
                              'or \"Low\", got %s of type %s', 
                              value, type(value))

    @staticmethod
    def to_object(d: dict) -> "ConveyorCarrierConf":
        inst = ConveyorCarrierConf(d['conveyor_carrier_speed'])
        return inst