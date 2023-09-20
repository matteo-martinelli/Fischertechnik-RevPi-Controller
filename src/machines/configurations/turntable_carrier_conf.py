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
    def turntable_carrier_speed(self): 
        return self._turntable_carrier_speed
    
    @turntable_carrier_speed.setter
    def turntable_carrier_speed(self, value: str): 
        if(value != "Low" or value != "Medium" or value != "High"):
            self.logger.error('Illegal value passed to the turntable ' +
                              'configuration. Expected a string, ' +
                              'got %s of value %s', value, type(value))
        else: 
            self._turntable_carrier_speed = value

    @staticmethod
    def to_object(d):
        inst = TurntableCarrierConf(d['turntable_carrier_speed'])
        return inst
