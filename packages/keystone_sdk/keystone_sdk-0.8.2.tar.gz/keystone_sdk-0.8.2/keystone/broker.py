# coding=utf-8

from __future__ import print_function
from six import with_metaclass
import abc
from datetime import datetime
import numpy as np

from keystone.api import keystone_class, api_method
from keystone.commission import KSCommissionModel
from keystone.slippage import KSSlippageModel
from keystone.constant import ORDER_ACCEPTED_MESSAGE, ORDER_FILLED_MESSAGE, ORDER_PARTIALLY_FILLED_MESSAGE
from keystone.order import (
                            KSTransaction, 
                            KSOrder,
                            KSOrderState,
                            KSOrderType,
                            KSOrderEvent,
                            KSOrderEventType
                            )
from keystone.universe import KSUniverse as Universe
from keystone.coordinator import KSCoordinator
from keystone.portfolio import KSPortfolio
from keystone.utils import math_utils

class KSBrokerPolicy(with_metaclass(abc.ABCMeta)):
    '''
    broker policy
    DO NOT use this class directlly
    '''
    def __init__(self, isInstantMatch = False, slippage = None, commission = None):
        self.isInstantMatch = isInstantMatch
        self.slippage = slippage
        self.commission = commission
        
    def setSlippageModel(self, model):
        if not isinstance(model, KSSlippageModel):
            raise TypeError("slippage model必须是继承自'KSSlippageModel'的实例对象。")
        self.slippage = model
        
    def setCommissionModel(self, model):
        if not isinstance(model, KSCommissionModel):
            raise TypeError("commission model必须是继承自'KSCommissionModel'的实例对象。")
        self.commission = model
        
    def turnOnInstantMatch(self):
        self.isInstantMatch = True
        
    @abc.abstractmethod
    def matchOrder(self, dataEvent, order, *args, **kwargs):
        pass
    
class KSDefaultBrokerPolicy(KSBrokerPolicy):
    def __init__(self):
        KSBrokerPolicy.__init__(self)
        
    def matchOrder(self, dataEvent, order, *args, **kwargs):
        sid = order.securityId()
        shares = order.remaining()
        dealPrice = dataEvent.query(sid, 'price')
        if np.isnan(dealPrice):
            return None
        
        # slippage
        if self.slippage is not None:
            dealPrice = self.slippage.compute(dataEvent, order)

        # commission
        commission = 0
        if self.commission is not None:
            commission = self.commission.compute(dataEvent, order)
        
        return KSTransaction(dataEvent.time(), order.orderid(), sid, shares, dealPrice, commission)
    

class KSBacktestingBroker(object):
    '''
    Backtesting Broker
    '''
    brokerPolicy = KSDefaultBrokerPolicy()

    def __init__(self, *args, **kwargs):
        self.openOrders = {}
        self.filledOrders = {}
        self.cancelledOrders = {}
        self.portfolio = KSPortfolio
        self.lastEvent = None
    
    def onDataEvent(self, dataEvent):
        self.lastEvent = dataEvent
        self.processAllOpenOrders(dataEvent)
    
    def registerOrder(self, order):
        self.openOrders[order.orderid()] = order
        
    def unregisterOrder(self, order):
        orderid = order.orderid()
        if orderid in self.openOrders:
            if order.state() == KSOrderState.FILLED:
                self.filledOrders[orderid] = order
            elif order.state() == KSOrderState.CANCELLED:
                self.cancelledOrders[orderid] = order
            else:
                pass
            self.openOrders.pop(orderid)
    
    # validate order
    def checkOrder(self, dataEvent, order):
        # 如果今天该sid不能交易则返回错误。例如停牌
        if order.sid() not in dataEvent.securities():
            return 'cannot trade for ' + order.sid() + ' in this time.'

        # 如果order数量为0，返回错误
        if order.total() == 0:
            return 'cannot place zero quantity order for ' + order.sid() + ' .'

        # 如果该order的话费超过手上的现金，返回错误
        # 还没实现，因为还没确定允不允许卖空

    def isExpiredOrder(self, order):
        return order.acceptedAt() < Universe.time
    
    def processAllOpenOrders(self, dataEvent):
        sortedOrders = self.getSortedOpenOrders()
        for order in sortedOrders:
            self.processOrder(dataEvent, order)
            
    def processOrder(self, dataEvent, order): 
        orderid = order.orderid()
        # Step 1 - check order content
        msg = self.checkOrder(dataEvent, order)
        if msg is not None:
            order.cancel(Universe.time, msg)
            self.unregisterOrder(order)
            self.notifyOrderEvent(orderid, KSOrderEventType.CANCELLED, order.cancelReason(), None)
            return

        # Step 2 - accept order
        if order.isSubmitted():
            order.accept(Universe.time)
            self.notifyOrderEvent(orderid, KSOrderEventType.ACCEPTED, ORDER_ACCEPTED_MESSAGE, None)
            
        # Step 3 - check and remove expired order
        if self.isExpiredOrder(order):
            order.cancel(Universe.time, 'order expired')
            self.unregisterOrder(order)
            self.notifyOrderEvent(orderid, KSOrderEventType.CANCELLED, order.cancelReason(), None)
            return
        
        # Step 4 - simulating transaction
        txn = self.brokerPolicy.matchOrder(dataEvent, order)
        # validate txn
        if txn is None:
            order.cancel(Universe.time, 'user txn is None, cancel order.')
            self.unregisterOrder(order)
            self.notifyOrderEvent(orderid, KSOrderEventType.CANCELLED, order.cancelReason(), None)
            return
        
        # Step 5 - update order info
        order.update(txn)
        if order.isFilled():
            self.notifyOrderEvent(orderid, KSOrderEventType.FILLED, ORDER_FILLED_MESSAGE, txn)
        else:
            self.notifyOrderEvent(orderid, KSOrderEventType.PARTIALLY_FILLED, ORDER_PARTIALLY_FILLED_MESSAGE, txn)
            
        if order.isCancelled() or order.isFilled():
            self.unregisterOrder(order)
            
    def getSortedOpenOrders(self):
        openOrders = list(self.openOrders.values())
        datetimes = [x.submittedAt() for x in openOrders]
        idx = np.argsort(datetimes)
        return [openOrders[i] for i in idx]
    
    def notifyOrderEvent(self, orderid, type, message, txn):
        orderEvent = KSOrderEvent(orderid, type, message, txn)
        KSCoordinator.dispatchOrderEvent(orderEvent)
        
    def getOrder(self, orderid):
        if orderid in self.openOrders:
            return self.openOrders[orderid]
        elif orderid in self.filledOrders:
            return self.filledOrders[orderid]
        elif orderid in self.cancelledOrders:
            return self.cancelledOrders[orderid]
        else:
            return None
        
    def submitOrder(self, sid, quantity, type = KSOrderType.MARKET_ORDER):
        order = KSOrder(sid, quantity, type)
        order.submit(Universe.time)
        self.registerOrder(order)
        
        if self.brokerPolicy.isInstantMatch:
            self.processOrder(self.lastEvent, order)
            
        return order.orderid()
    
    def order(self, sid, quantity, type = KSOrderType.MARKET_ORDER):
        return self.submitOrder(sid, quantity, type)
    
    def orderValue(self, sid, value, type = KSOrderType.MARKET_ORDER):
        price = Universe.getPrice(sid)
        shares = np.floor(np.abs(value) / price)*np.sign(value)
        assert(np.isnan(shares)==False)
        return self.submitOrder(sid, shares, type)
    
    def orderPercentage(self, sid, percentage, type = KSOrderType.MARKET_ORDER):
        return self.orderValue(sid, self.portfolio.value() * percentage, type)
    
    def orderTarget(self, sid, targetShares, type = KSOrderType.MARKET_ORDER):
        curShares = 0
        if self.portfolio.hasPosition(sid):
            curShares = self.portfolio.getPosition(sid).quantity()
        return self.submitOrder(sid, targetShares - curShares, type)
        
    def orderTargetValue(self, sid, targetValue, type = KSOrderType.MARKET_ORDER):
        curValue = 0
        if self.portfolio.hasPosition(sid):
            if math_utils.tolerant_equals(targetValue, 0):
                quantity = self.portfolio.getPosition(sid).quantity()
                return self.submitOrder(sid, -quantity, type)
            curValue = self.portfolio.getPosition(sid).value()
        return self.orderValue(sid, targetValue - curValue, type)
    
    def orderTargetPercentage(self, sid, percentage, type = KSOrderType.MARKET_ORDER):
        return self.orderTargetValue(sid, self.portfolio.value() * percentage, type)
    
    def cancelOrder(self, orderid):
        if orderid in self.openOrders:
            order = self.openOrders[orderid]
            order.cancel(Universe.time, "cancelled by user")
            self.unregisterOrder(order)