#!/usr/bin/env python

"""
compressor_service_conf.py: CompressorServiceConf class

Contains and represents the compressor service configuration
"""

import logging


class CompressorServiceConf(object):
    def __init__(self, compressor_behaviour: str):
        self._compressor_behaviour = compressor_behaviour
        
        self.logger = logging.getLogger('multiproc_dept_logger')
        
    @property
    def compressor_behaviour(self) -> str: 
        return self._compressor_behaviour
    
    @compressor_behaviour.setter
    def oven_processing_time(self, value:str) -> None: 
        if(value == "always_on" or value == "when_needed"):
            self._compressor_behaviour = value
        else: 
            self.logger.error('Illegal value passed to the conveyor ' +
                              'configuration. Expected \"always_on\" ' + 
                              'or \"when_needed\", got %s of type %s', 
                              value, type(value))

    @staticmethod
    def to_object(d) -> "CompressorServiceConf":
        inst = CompressorServiceConf(d['motor_behaviour'])
        return inst
