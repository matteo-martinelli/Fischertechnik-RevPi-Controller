#!/usr/bin/env python

"""
oven_station_conf.py: OvenStationConf class

Contains and represents the oven station configuration
"""

class OvenStationConf(object):
    def __init__(self, oven_processing_time: int):
        self._oven_processing_time = oven_processing_time
         #self.type = 'OvenStationConf'
        
    @property
    def oven_processing_time(self): 
        return self._oven_processing_time
    
    @oven_processing_time.setter
    def oven_processing_time(self, value: int): 
        self._oven_processing_time = value

    #def __str__(self):
    #    details = ''
    #    details += f'Oven processing time: {self.oven_processing_time}\n'
    #    return details

    @staticmethod
    def to_object(d):
        inst = OvenStationConf(d['oven_processing_time'])
        return inst