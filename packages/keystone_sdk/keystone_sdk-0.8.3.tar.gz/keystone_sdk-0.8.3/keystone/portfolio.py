# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime
import numpy as np

from keystone.universe import KSUniverse as Universe
from keystone.parameters import DEFAULT_STARTING_CASH

class KSPosition(object):
    def __init__(self, security, quantity, price, commission):
        self.__security = security
        self.__quantity = quantity
        self.__priceArray = [price]
        self.__quantityArray = [quantity]
        self.__commissionArray = [commission]
        self.__datetimeArray = [Universe.time]
        self.__openAt = Universe.time
        self.__valueArray = [self.value()]
    
    def update(self, quantity, price, commission):
        self.__quantity += quantity
        self.__priceArray.append(price)
        self.__commissionArray.append(commission)
        self.__datetimeArray.append(Universe.time)
    
    def to_dict(self):
        history = []
        for commission, price, quantity, dt, value in zip(
            self.__commissionArray,
            self.__priceArray, 
            self.__quantityArray, 
            self.__datetimeArray,
            self.__valueArray):
            history.append({
                'datetime': dt,
                'quantity': quantity,
                'price': price,
                'commission': commission,
                'value': value
                })

        return {'sid': self.__security,
                'quantity': self.__quantity,
                'value': self.value(),
                'open_at': self.__openAt,
                'avg_cost': self.costBasis(),
                'total_commission': self.totalCommission(),
                'avg_commission': self.avgCommission(),
                'history': history}

    def __repr__(self):
        return self.to_dict().__repr__()
    
    def __str__(self):
        return self.to_dict().__str__()

    def isShort(self):
        return self.__quantity < 0
    
    def costBasis(self):
        return np.mean(self.__priceArray)
    
    def avgCommission(self):
        return np.mean(self.__commissionArray)

    def totalCommission(self):
        return np.sum(self.__commissionArray)

    def security(self):
        return self.__security
    
    
    def quantity(self):
        return self.__quantity
    
    
    def value(self):
        price = Universe.getPrice(self.__security)
        assert price is not None
        assert not np.isnan(price)
        return self.__quantity * price
    
    
    def openAt(self):
        return self.__openAt
    

class KSPortfolio(object):
    '''
    portfolio
    '''
    __startingCash = DEFAULT_STARTING_CASH
    __cash = DEFAULT_STARTING_CASH
    __positions = {}

    def __init__(self):
        pass
    
    @classmethod
    def update(self, security, quantity, price, commission):
        if security in self.__positions:
            self.__positions[security].update(quantity, price, commission)
            if self.__positions[security].quantity() == 0:
                self.__positions.pop(security)
        else:
            self.__positions[security] = KSPosition(security, quantity, price, commission)
        
        # TODO: 做空时计算方法要变
        self.__cash = self.__cash - (price * quantity) - commission
        
        # assert self.__cash >= 0.0
    
    @classmethod
    def startingCash(self):
        return self.__startingCash
        

    @classmethod
    def cash(self):
        return self.__cash
    
    
    @classmethod
    def securities(self):
        return list(self.__positions.keys())
    
    
    @classmethod
    def hasPosition(self, security):
        return security in self.__positions
    
    
    @classmethod
    def getPosition(self, security):
        if security in self.__positions:
            return self.__positions[security]
        else:
            raise KeyError("no such position for '" + security + u"'.")
      
    @classmethod      
    def positions(self):
        return list(self.__positions.values())
       
    @classmethod 
    def value(self):
        return self.__cash + np.sum([pos.value() for pos in list(self.__positions.values())])
    