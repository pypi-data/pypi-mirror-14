# -*- coding: utf-8 -*-

from __future__ import print_function
from keystone.utils import math_utils
from keystone.api import keystone_class, api_method
from keystone.order import KSOrderType
from keystone.broker import KSBacktestingBroker
from keystone.portfolio import KSPortfolio
from keystone.history import KSHistory
from keystone.performance.analyzer import KSAnalyzer
from keystone.py3compat import PY3, builtin_mod, iteritems, unicode_type, string_types


class KSContext(object):
    def __init__(self, history = None, analyzers = None):
        # assert isinstance(portfolio, KSPortfolio)
        self.portfolio = KSPortfolio
        if history is not None:
            assert isinstance(history, KSHistory)
            self.history = history
        if analyzers is not None:
            for analyzer in analyzers:
                assert isinstance(analyzer, KSAnalyzer)
            self.analyzers = analyzers
    
class KSAction(object):
    def __init__(self, broker, logger = None):
        assert isinstance(broker, KSBacktestingBroker)
        self.__broker = broker
        self.__logger = logger
    
    
    def order(self, sid, amount, type = KSOrderType.MARKET_ORDER):
        if not isinstance(sid, string_types):
            raise TypeError("sid格式错误，sid必须为字符串。")
        
        if not math_utils.isint(amount):
            raise TypeError("amount格式错误，amount必须为整数。")
        
        return self.__broker.order(sid, amount, type)
        
    
    def orderValue(self, sid, value, type = KSOrderType.MARKET_ORDER):
        if not isinstance(sid, string_types):
            raise TypeError("sid格式错误，sid必须为字符串。")
        
        if not math_utils.isnumber(value):
            raise TypeError("value格式错误，value必须为数字。")
        
        return self.__broker.orderValue(sid, value, type)
        
    
    def orderPercentage(self, sid, percentage, type = KSOrderType.MARKET_ORDER):
        if not isinstance(sid, string_types):
            raise TypeError("sid格式错误，sid必须为字符串。")
        
        if not math_utils.isnumber(percentage) or abs(percentage) > 1.0:
            raise TypeError("percentage格式错误，percentage必须为[-1.0,1.0]。")
        
        return self.__broker.orderPercentage(sid, percentage, type)
        
    
    def orderTarget(self, sid, amount, type = KSOrderType.MARKET_ORDER):
        if not isinstance(sid, string_types):
            raise TypeError("sid格式错误，sid必须为字符串。")
        
        if not math_utils.isint(amount):
            raise TypeError("amount格式错误，amount必须为整数。")
        
        return self.__broker.orderTarget(sid, amount, type)
        
    
    def orderTargetValue(self, sid, value, type = KSOrderType.MARKET_ORDER):
        if not isinstance(sid, string_types):
            raise TypeError("sid格式错误，sid必须为字符串。")
        
        if not math_utils.isnumber(value):
            raise TypeError("value格式错误，value必须为数字。")
        
        return self.__broker.orderTargetValue(sid, value, type)
        
    
    def orderTargetPercentage(self, sid, percentage, type = KSOrderType.MARKET_ORDER):
        if not isinstance(sid, string_types):
            raise TypeError("sid格式错误，sid必须为字符串。")
        
        if not math_utils.isnumber(percentage) or abs(percentage) > 1.0:
            raise TypeError("percentage格式错误，percentage必须为[-1.0,1.0]。")
        
        return self.__broker.orderTargetPercentage(sid, percentage, type)
    
    
    def getOrder(self, orderid):
        return self.__broker.getOrder(orderid)