# -*- coding: utf-8 -*-

from __future__ import print_function
from six import with_metaclass
import abc
import numpy as np
from datetime import datetime

from keystone.api import keystone_class, api_method
from keystone.utils import math_utils

class KSCommissionModel(with_metaclass(abc.ABCMeta)):
    def __init__(self):
        pass
    
    @abc.abstractmethod
    def compute(self, dataEvent, order, *args, **kwargs):
        '''
        INPUT:
            dataEvent - Current data event
            order - KSOrder instance about the current order
            args - User custom args
            kwargs - User custom kwargs
        OUTPUT:
            user MUST return a commission
        '''
        return 0
    
class KSPerShareCommissionModel(KSCommissionModel):
    def __init__(self, rate):
        KSCommissionModel.__init__(self)
        if not math_utils.isnumber(rate):
            raise TypeError("rate必须为数字。")
        self.rate = rate
        
    def compute(self, dataEvent, order, *args, **kwargs):
        shares = order.remaining()
        return abs(shares) * self.rate
    
class KSTransactionValueCommissionModel(KSCommissionModel):
    def __init__(self, rate):
        KSCommissionModel.__init__(self)
        if not math_utils.isnumber(rate):
            raise TypeError("rate必须为数字。")
        self.rate = rate
    
    def compute(self, dataEvent, order, *args, **kwargs):
        shares = order.remaining()
        price = dataEvent.query(sid, 'price')
        return abs(shares * price * self.rate)

