#!/usr/bin/env python

"""
vacuum_carrier_conf.py: VacuumCarrierConf class

Contains and represents the vacuum carrier configuration
"""

import logging


class VacuumCarrierConf(object):
    def __init__(self, vacuum_carrier_speed: str):
        self._vacuum_carrier_speed = vacuum_carrier_speed

        self.logger = logging.getLogger('multiproc_dept_logger')
        
    @property
    def vacuum_carrier_speed(self) -> str: 
        return self._vacuum_carrier_speed
    
    @vacuum_carrier_speed.setter
    def vacuum_carrier_speed(self, value: str) -> None: 
        if(value == "Low" or value == "Medium" or value == "High"):
            self._vacuum_carrier_speed = value
        else: 
            self.logger.error('Illegal value passed to the vacuum carrier ' +
                              'configuration. Expected \"High\", \"Medium\" ' + 
                              'or \"Low\", got %s of type %s', 
                              value, type(value))

    @staticmethod
    def to_object(d: dict) -> "VacuumCarrierConf":
        inst = VacuumCarrierConf(d['vacuum_carrier_speed'])
        return inst