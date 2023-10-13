#!/usr/bin/env python

"""
turntable_carrier_conf.py: TurntableCarrierConf class

Contains and represents the turntable carrier configuration
"""

import logging


class TurntableCarrierConf(object):
    def __init__(self, turntable_carrier_speed: str):
        self._turntable_carrier_speed = turntable_carrier_speed
        
        self.logger = logging.getLogger('multiproc_dept_logger')
        
    @property
    def turntable_carrier_speed(self) -> str: 
        return self._turntable_carrier_speed
    
    @turntable_carrier_speed.setter
    def turntable_carrier_speed(self, value: str) -> None: 
        if(value == "Low" or value == "Medium" or value == "High"):
            self._turntable_carrier_speed = value
        else: 
            self.logger.error('Illegal value passed to the turntable ' +
                              'configuration. Expected \"High\", \"Medium\" ' + 
                              'or \"Low\", got %s of type %s', 
                              value, type(value))

    @staticmethod
    def to_object(d: dict) -> "TurntableCarrierConf":
        inst = TurntableCarrierConf(d['turntable_carrier_speed'])
        return inst
