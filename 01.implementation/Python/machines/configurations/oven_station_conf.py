
#!/usr/bin/env python

"""
multiproc_dept_conf.py: MultiProcDeptConf class
"""


from conf.mqtt_conf_parameters import MqttConfiguratorParameter
import paho.mqtt.client as mqtt
import json

class OvenStationConf(object):
    """Configuration class storing information about the department 
    configuration setting.    
    """

    def __init__(self, oven_processing_time: int):
        self._oven_processing_time = oven_processing_time
        
    @property
    def oven_processing_time(self): 
        return self._oven_processing_time
    
    @oven_processing_time.setter
    def oven_processing_time(self, value: int): 
        self._oven_processing_time = value
