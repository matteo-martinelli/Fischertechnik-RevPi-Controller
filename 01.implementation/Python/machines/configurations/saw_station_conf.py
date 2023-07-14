#!/usr/bin/env python

"""
saw_station_conf.py: SawStationConf class

Contains and represents the saw station configuration
"""

class SawStationConf(object):
    def __init__(self, saw_processing_time: int):
        self._saw_processing_time = saw_processing_time
        
    @property
    def saw_processing_time(self): 
        return self._saw_processing_time
    
    @saw_processing_time.setter
    def saw_processing_time(self, value: int): 
        self._saw_processing_time = value
