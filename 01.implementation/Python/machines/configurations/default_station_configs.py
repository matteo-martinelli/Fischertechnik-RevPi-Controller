#!/usr/bin/env python

"""
default_station_configs.py: DefaultStationsConfigs class

Contains constants for initialising machine stations configurations
"""


class DefaultStationsConfigs(object):
    PIECES_TO_PRODUCE = 4
    COMPRESSOR_BEHAVIOUR = 'always_on'
    OVEN_PROCESSING_TIME = 1
    SAW_PROCESSING_TIME = 1
    VACUUM_CARRIER_SPEED = 1
    TURNTABLE_CARRIER_SPEED = 1

    def __init__(self):
        self.description = 'Default configuration values for multiproc_dept'
