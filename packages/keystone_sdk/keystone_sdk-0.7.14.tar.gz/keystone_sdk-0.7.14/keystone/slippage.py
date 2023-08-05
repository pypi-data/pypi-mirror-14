# -*- coding: utf-8 -*-

from __future__ import print_function
from six import with_metaclass
import abc
import numpy as np
from datetime import datetime

from keystone.api import keystone_class, api_method
from keystone.utils import math_utils

class KSSlippageModel(with_metaclass(abc.ABCMeta)):
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
            user MUST return a deal price
        '''
        return 0
    
class KSFixedSlippageModel(KSSlippageModel):
    def __init__(self, rate):
        KSSlippageModel.__init__(self)
        if not math_utils.isnumber(rate) or rate < 0 or rate > 1:
            raise TypeError("rate必须为数字，且 0 <= rate <= 1。")
        self.spread = rate
    
    def compute(self, dataEvent, order, *args, **kwargs):
        sid = order.securityId()
        shares = order.remaining()
        dealPrice = dataEvent.query(sid, 'price')
        direction = np.sign(shares)

        return dealPrice * (1 + self.spread / 2 * direction)
