#!/usr/bin/env python

"""
compressor_service_conf.py: CompressorServiceConf class

Contains and represents the compressor service configuration
"""


class CompressorServiceConf(object):
    def __init__(self, compressor_behaviour: str):
        self._compressor_behaviour = compressor_behaviour
        
    @property
    def compressor_behaviour(self): 
        return self._compressor_behaviour
    
    @compressor_behaviour.setter
    def oven_processing_time(self, value: str): 
        self._compressor_behaviour = value
