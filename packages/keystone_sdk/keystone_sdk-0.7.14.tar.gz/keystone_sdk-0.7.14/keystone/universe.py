# -*- coding: utf-8 -*-

from __future__ import print_function
from keystone.api import keystone_class, api_method
from datetime import datetime
import numpy as np
from keystone.coordinator import KSObserver

class KSUniverse(KSObserver):
    '''
    Universe infomations about security and current backtesting time
    '''
    time = None
    price = {}
    latestDataEvent = None
    def __init__(self):
        KSObserver.__init__(self)
        
    @classmethod
    def getPrice(cls, security):
        if security in cls.price:
            return cls.price[security]
        else:
            return np.nan
    
    @classmethod
    def onDataEvent(cls, dataEvent):
        # update time
        cls.time = dataEvent.time()
        
        # update latest dataEvent
        cls.latestDataEvent = dataEvent
        
        # update price
        securities = dataEvent.securities()
        if len(securities) == 0:
            return
        latestPrice = dataEvent.query(securities, 'price')
        if len(securities) == 1:
            cls.price[securities[0]] = latestPrice
        else:
            cls.price.update(latestPrice.to_dict())