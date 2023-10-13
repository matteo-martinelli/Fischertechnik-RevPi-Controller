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
    def pieces_to_produce(self) -> int:
        return self._pieces_to_produce
    
    @pieces_to_produce.setter
    def pieces_to_produce(self, value: int) -> None:
        if (value > 0):
            self._pieces_to_produce = value
        else: 
            self.logger.error('Wron pieces to produce value; expected a ' + 
                              'positive int, got %s of type %s', 
                              value, type(value))
    
    @staticmethod
    def to_object(d) -> "MultiProcDeptConf":
        inst = MultiProcDeptConf(d['pieces_to_produce'])
        return inst
