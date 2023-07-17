#!/usr/bin/env python

"""
vacuum_carrier_conf.py: VacuumCarrierConf class

Contains and represents the vacuum carrier configuration
"""

class VacuumCarrierConf(object):
    def __init__(self, vacuum_carrier_speed: int):
        self._vacuum_carrier_speed = vacuum_carrier_speed
        
    @property
    def vacuum_carrier_speed(self): 
        return self._vacuum_carrier_speed
    
    @vacuum_carrier_speed.setter
    def vacuum_carrier_speed(self, value: int): 
        self._vacuum_carrier_speed = value

    @staticmethod
    def to_object(d):
        inst = VacuumCarrierConf(d['vacuum_carrier_speed_pwm'])
        return inst