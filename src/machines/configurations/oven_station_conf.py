#!/usr/bin/env python

"""
oven_station_conf.py: OvenStationConf class

Contains and represents the oven station configuration
"""

class OvenStationConf(object):
    def __init__(self, oven_processing_time: int):
        self._oven_processing_time = oven_processing_time
        
    @property
    def oven_processing_time(self) -> int: 
        return self._oven_processing_time
    
    @oven_processing_time.setter
    def oven_processing_time(self, value: int) -> None: 
        self._oven_processing_time = value

    @staticmethod
    def to_object(d) -> "OvenStationConf":
        inst = OvenStationConf(d['oven_processing_time'])
        return inst