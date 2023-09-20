#!/usr/bin/env python

"""
default_station_configs.py: DefaultStationsConfigs class

Contains constants for initialising machine stations configurations

The configuration stored here set various aspects of the Fischertechnik runtime
behaviours. 

  - PIECES_TO_PRODUCE:          sets pieces to produce; this value is compared 
                                to the variable that counts pieces done to 
                                understand if the batch requested is completed
  - COMPRESSOR_BEHAVIOUR:       always_on => always on during operations
                                on_request => turned on and off when requested 
                                something_else => another value (used only for 
                                dev and test purposes)
  - OVEN_PROCESSING_TIME:       1 => seconds to keep the product in heating 
                                phase at target temp
  - SAW_PROCESSING_TIME:        1 => seconds to keep the product in heating 
                                phase at target temp
  - VACUUM_CARRIER_SPEED:       speed at which the carrier works; the speed 
                                increase and decrease is simulated through one 
                                or more stops; target values are "low", 
                                "medium", "high
  - TURNTABLE_CARRIER_SPEED:    speed at which the carrier works; the speed 
                                increase and decrease is simulated through one 
                                or more stops; target values are "low", 
                                "medium", "high
"""

class DefaultStationsConfigs(object):
    PIECES_TO_PRODUCE = 4                       # pieces
    COMPRESSOR_BEHAVIOUR = 'something_else'     # string
    OVEN_PROCESSING_TIME = 1                    # seconds
    SAW_PROCESSING_TIME = 1                     # seconds
    VACUUM_CARRIER_SPEED = "Low"                # string
    TURNTABLE_CARRIER_SPEED = "High"            # string
    CONVEYOR_CARRIER_SPEED = "High"             # string

    def __init__(self):
        self.description = 'Default configuration values for multiproc_dept'
