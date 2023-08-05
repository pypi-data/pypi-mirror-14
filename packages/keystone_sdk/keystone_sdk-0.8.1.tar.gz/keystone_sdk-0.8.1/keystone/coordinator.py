# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import pandas as pd
import sys
from six import with_metaclass
import abc

from keystone.api import keystone_class, api_method
# from keystone.engine import KSEventEngine
from keystone.engine.ksevent_engine import KSEventEngine

class KSObserver(with_metaclass(abc.ABCMeta)):
    
    @abc.abstractmethod
    def onDataEvent(self, dataEvent):
        pass
    
    def onOrderEvent(self, orderEvent):
        pass
    

class KSCoordinator(object):
    '''
    Global Event Dispatcher
    '''
    
    # pass pd.Series function handler to KSEventEngine,
    # enable cpp interface KSDataEvent.query call pd.Series
    # function and return a pd.Series object 

    # self.eventEngine = KSEventEngine(pd.DataFrame)
    # eventEngine = KSEventEngine(pd.Series)
    eventEngine = KSEventEngine()
    dataObservers = []
    orderObservers = []
    
    @classmethod
    def addSource(cls, source):
        cls.eventEngine.addSource(source)

    @classmethod
    def addDataObserver(cls, observer):
        cls.dataObservers.append(observer)
    
    @classmethod
    def addOrderObserver(cls, observer):
        cls.orderObservers.append(observer)
        
    @classmethod
    def dispatchDataEvent(cls, dataEvent):
        for observer in cls.dataObservers:
            observer.onDataEvent(dataEvent)
    
    @classmethod 
    def dispatchOrderEvent(cls, orderEvent):
        for observer in cls.orderObservers:
            observer.onOrderEvent(orderEvent)
    
    @classmethod
    def run(cls):
        for dataEvent in cls.eventEngine.dataEvent:
            cls.dispatchDataEvent(dataEvent)
        # cls.eventEngine.run();
        # while 1:
        #     dataEvent = cls.eventEngine.getNextEvent()
        #     if dataEvent is None:
        #         break
        #     else:
        #         cls.dispatchDataEvent(dataEvent)
            