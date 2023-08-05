# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime
import numpy as np
from keystone.utils import math_utils
from copy import copy

class KSOrderType(object):
    MARKET_ORDER = 'MARKET_ORDER'
    LIMIT_ORDER = 'LIMIT_ORDER'
    STOP_ORDER = 'STOP_ORDER'
    STOP_LIMIT_ORDER = 'STOP_LIMIT_ORDER'
    
class KSOrderState:
    INITIAL = 'INITIAL'
    SUBMITTED = 'SUBMITTED'
    ACCEPTED = 'ACCEPTED'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED = 'FILLED'
    CANCELLED = 'CANCELLED'

class KSOrderEventType:
    SUBMITTED = 'SUBMITTED'
    ACCEPTED = 'ACCEPTED'
    PARTIALLY_FILLED = 'PARTIALLY_FILLED'
    FILLED = 'FILLED'
    CANCELLED = 'CANCELLED'


class KSTransaction(object):
    def __init__(self, dt, orderid, sid, quantity, price, commission):
        self.time = dt
        self.orderid = orderid
        self.sid = sid
        self.quantity = quantity
        self.price = price
        self.commission = commission
        
    def to_dict(self):
        fields = copy(self.__dict__)
        return fields
    
    def __repr__(self):
        return self.to_dict().__repr__()
    
    def __str__(self):
        return self.to_dict().__str__()
        

class KSOrder(object):
    def __init__(self, sid, quantity, type = KSOrderType.MARKET_ORDER):
        self.__orderid = math_utils.generate_uuid()
        self.__sid = sid
        self.__quantity = quantity
        self.__type = type
        self.__filled = 0
        self.__avgFilledPrice = 0
        self.__filledPrices = []
        self.__filledQuantities = []
        self.__filledCommissions = []
        self.__state = KSOrderState.INITIAL
        self.__submitTime = None
        self.__acceptTime = None
        self.__updateTime = None
        self.__cancelTime = None
        self.__reason = ''
        
    def __str__(self):
        info = "Order [" + str(self.__orderid) + "]:\n" + \
        "security:\t" + str(self.__sid) + "\n" + \
        "quantity:\t" + str(self.__quantity) + "\n" + \
        "type:\t" + str(self.__type) + "\n" + \
        "filled:\t" + str(self.__filled) + "\n" + \
        "submitTime:\t" + str(self.__submitTime) + "\n" + \
        "acceptTime:\t" + str(self.__acceptTime) + "\n" + \
        "updateTime:\t" + str(self.__updateTime) + "\n" + \
        "cancelTime:\t" + str(self.__cancelTime) + "\n" + \
        "cancelReason:\t" + self.__reason + "\n"
        return info
    
    
    def orderid(self):
        return self.__orderid
    
    
    def sid(self):
        return self.__sid
    
    
    def type(self):
        return self.__type

    
    def state(self):
        return self.__state
    
    
    def securityId(self):
        return self.__sid
    
    
    def total(self):
        return self.__quantity
    
    
    def filled(self):
        return self.__filled
    
    
    def remaining(self):
        return self.__quantity - self.__filled
    
    
    def isSubmitted(self):
        return self.__state == KSOrderState.SUBMITTED
    
    
    def isFilled(self):
        return self.__state == KSOrderState.FILLED
    
    
    def isPratiallyFilled(self):
        return self.__state == KSOrderState.PARTIALLY_FILLED
    
    
    def isCancelled(self):
        return self.__state == KSOrderState.CANCELLED
        
    
    def isSell(self):
        return self.__quantity < 0
    
    
    def submittedAt(self):
        return self.__submitTime
    
    
    def acceptedAt(self):
        return self.__acceptTime
    
    
    def cancelledAt(self):
        return self.__cancelTime
    
    
    def cancelReason(self):
        return self.__reason
    
    
    def avgPrice(self):
        return self.__avgFilledPrice
    
    
    def avgCommission(self):
        return np.mean(self.__filledCommissions)
    
    
    def totalCommission(self):
        return np.sum(self.__filledCommissions)
    
    def setState(self, state):
        self.__state = state
        
    def submit(self, time):
        if self.__state == KSOrderState.INITIAL:
            self.__state = KSOrderState.SUBMITTED
            self.__submitTime = time
        
    def accept(self, time):
        self.__state = KSOrderState.ACCEPTED
        self.__acceptTime = time
    
    def cancel(self, time, reason = ''):
        self.__state = KSOrderState.CANCELLED
        self.__cancelTime = time
        self.__reason = reason
    
    # may raise error, since txn may constructed by user 
    # TODO: 后续支持自定义txn，记得修改错误为中文。   
    def update(self, txn):
        if not isinstance(txn, KSTransaction):
            raise TypeError("txn MUST be a instance of KSTransaction")
        
        if np.sign(txn.quantity) != np.sign(self.__quantity):
            raise TypeError("direction of txn is NOT consistent with this order")
        
        if np.abs(txn.quantity + self.__filled) > np.abs(self.__quantity):
            raise TypeError("txn invalid, np.abs(txn.quantity + self.__filled) > self.__quantity")
        
        self.__filled += txn.quantity
        
        self.__filledPrices.append(txn.price)
        self.__filledQuantities.append(txn.quantity)
        self.__filledCommissions.append(txn.commission)
        
        self.__avgFilledPrice = (np.array(self.__filledPrices) * self.__filledQuantities)/np.sum(self.__filledQuantities)
        
        if self.remaining() == 0:
            self.__state = KSOrderState.FILLED
        else:
            self.__state = KSOrderState.PARTIALLY_FILLED
        
        self.__updateTime = txn.time



class KSOrderEvent(object):
    def __init__(self, orderid, type, message, txn):
        self.orderid = orderid
        self.type = type
        self.message = message
        self.txn = txn
    
    def to_dict(self):
        fields = copy(self.__dict__)
        return fields
    
    def __repr__(self):
        return self.to_dict().__repr__()
    
    def __str__(self):
        return self.to_dict().__str__()
        
