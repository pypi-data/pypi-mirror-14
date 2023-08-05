# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import deque, Iterable
import pandas as pd
import numpy as np

from keystone.utils import math_utils
from keystone.api import keystone_class, api_method
from keystone.coordinator import KSObserver
from keystone.py3compat import PY3, builtin_mod, iteritems, unicode_type, string_types
import datetime


class KSHistory(KSObserver):
    def __init__(self, capacity):
        if not math_utils.isint(capacity) or capacity == 0:
            raise TypeError("capacity格式错误，capacity必须为非0整数。")
        self.__capacity = capacity
        self.__data = deque([],capacity)
        
    
    def query(self, startTime, endTime, ids, fieldname):
        # print "[startTime,endTime] = [" + str(startTime) + "," + str(endTime) +"]"
        # Check parameters
        if not isinstance(startTime, datetime.datetime):
            raise TypeError("startTime格式错误，startTime必须为datetime类型。")
        
        if not isinstance(endTime, datetime.datetime):
            raise TypeError("endTime格式错误，endTime必须为datetime类型。")
        
        if not isinstance(fieldname, string_types):
            raise TypeError("fieldname格式错误, fieldname必须是字符串。")
        
        if not isinstance(ids, string_types) and not isinstance(ids, Iterable):
            raise TypeError("securities格式错误, securities必须是字符串或字符串数组。")

        if isinstance(ids, string_types):
            ids = [ids]

        if isinstance(ids, Iterable):
            for x in ids:
                if not isinstance(x, string_types):
                        raise TypeError("securities格式错误, securities必须是字符串或字符串数组。")
        
        # Determine size m
        m = 0
        iter = []
        for i in range(len(self.__data)):
            dt = self.__data[i].time()
            if startTime <= dt and dt <=endTime:
                m += 1
                iter.append(i)

        # Query
        ret = pd.DataFrame(np.empty((len(ids), m)), index=ids)
        column_idx = 0
        for i in iter:
            s = self.__data[i].query(ids, fieldname)
            if not isinstance(s, pd.Series):
                s = pd.Series(s, index = ids)
            ret[column_idx] = s
            ret.rename(columns={column_idx:self.__data[i].time()},inplace=True) 
            column_idx += 1
            
        return ret
    
    def queryN(self, n, ids, fieldname):
        # Check parameters
        if not math_utils.isint(n) or n == 0:
            raise TypeError("n格式错误，n必须为非0整数。")
        
        if not isinstance(fieldname, string_types):
            raise TypeError("fieldname格式错误, fieldname必须是字符串。")
        
        if not isinstance(ids, string_types) and not isinstance(ids, Iterable):
            raise TypeError("securities格式错误, securities必须是字符串或字符串数组。")
        
        if isinstance(ids, string_types):
            ids = [ids]

        if isinstance(ids, Iterable):
            for x in ids:
                if not isinstance(x, string_types):
                        raise TypeError("securities格式错误, securities必须是字符串或字符串数组。")
        
        # QueryN
        m = min(n, len(self.__data))
        iter = range(len(self.__data) - m, len(self.__data))
        ret = pd.DataFrame(np.empty((len(ids), m)), index=ids)
        column_idx = 0
        for i in iter:
            s = self.__data[i].query(ids, fieldname)
            if not isinstance(s, pd.Series):
                s = pd.Series(s, index = ids)
            ret[column_idx] = s
            ret.rename(columns={column_idx:self.__data[i].time()},inplace=True) 
            column_idx += 1
            
        return ret
    
    def onDataEvent(self, dataEvent):
        self.__data.append(dataEvent)
    