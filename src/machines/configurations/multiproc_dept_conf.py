#!/usr/bin/env python

"""
multiproc_dept_conf.py: MultiProcDeptConf class
"""


class MultiProcDeptConf(object):
    """Configuration class storing information about the department 
    configuration setting.    
    """

    #def __init__(self, pieces_to_produce=0, compressor_behaviour="always_on",
    #             oven_processing_time=0, saw_processing_time=0, 
    #             vacuum_carrier_speed=0, turntable_carrier_speed=0):
    def __init__(self, pieces_to_produce=0):
        self._pieces_to_produce = pieces_to_produce
        #self._compressor_behaviour = compressor_behaviour
        #self._oven_processing_time = oven_processing_time
        #self._saw_processing_time = saw_processing_time
        #self._vacuum_carrier_speed = vacuum_carrier_speed
        #self._turntable_carrier_speed = turntable_carrier_speed

    @property
    def pieces_to_produce(self):
        return self._pieces_to_produce
    
    @pieces_to_produce.setter
    def pieces_to_produce(self, value: int):
        self._pieces_to_produce = value
    
    @property
    def compressor_behaviour(self): 
        return self._compressor_behaviour
    
    @compressor_behaviour.setter
    def compressor_behaviour(self, value: str):
        self._compressor_behaviour = value

    @property
    def oven_processing_time(self): 
        return self._oven_processing_time
    
    @oven_processing_time.setter
    def oven_processing_time(self, value: int): 
        self._oven_processing_time = value

    @property
    def saw_processing_time(self):
        return self._saw_processing_time
    
    @saw_processing_time.setter
    def saw_processing_time(self, value: int):
        self._saw_processing_time = value

    @property
    def vacuum_carrier_speed(self):
        return self._vacuum_carrier_speed
    
    @vacuum_carrier_speed.setter
    def vacuum_carrier_speed(self, value: int):
        self._vacuum_carrier_speed = value

    @property
    def turntable_carrier_speed(self):
        return self._turntable_carrier_speed
    
    @turntable_carrier_speed.setter
    def turntable_carrier_speed(self, value: int):
        self._turntable_carrier_speed = value

    @staticmethod
    def to_object(d):
        inst = MultiProcDeptConf(d['pieces_to_produce']#, 
                                 #d['compressor_behaviour'], 
                                 #d['oven_processing_time'], 
                                 #d['saw_processing_time'], 
                                 #d['vacuum_carrier_speed_pwm'], 
                                 #d['turntable_carrier_speed_pwm']
                                )
        return inst
