#!/usr/bin/env python

"""
multiproc_dept_conf.py: MultiProcDeptConf class
"""

import logging


class MultiProcDeptConf(object):
    """Configuration class storing information about the department 
    configuration setting.    
    """

    def __init__(self, pieces_to_produce=0):
        self._pieces_to_produce = pieces_to_produce
        self.logger = logging.getLogger('multiproc_dept_logger')

    @property
    def pieces_to_produce(self):
        return self._pieces_to_produce
    
    @pieces_to_produce.setter
    def pieces_to_produce(self, value: int):
        if (value > 0):
            self._pieces_to_produce = value
        else: 
            self.logger.error('Wron pieces to produce value; expected a ' + 
                              'positive int, got %s of type %s', 
                              value, type(value))
    
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
