# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import pandas as pd
import sys
from keystone.py3compat import PY3, builtin_mod, iteritems, unicode_type, string_types

class KSBaseSource(dict):
    ''' KSBaseSource for user data '''
    def tagAsPriceData(self, securityColumn, priceColumn):
        if not isinstance(securityColumn, string_types):
            raise TypeError("securityColumn格式错误, securityColumn必须是字符串。")
        if not isinstance(priceColumn, string_types):
            raise TypeError("priceColumn格式错误, priceColumn必须是字符串。")
        self['sid_column'] = securityColumn
        self['price_column'] = priceColumn

    def tagAsSecurityData(self, securityColumn):
        if not isinstance(securityColumn, string_types):
            raise TypeError("securityColumn格式错误, securityColumn必须是字符串。")
        self['sid_column'] = securityColumn

    def setDateFormat(self, dateFormat):
        if not isinstance(dateFormat, string_types):
            raise TypeError("dateFormat格式错误, dateFormat必须是字符串。")
        self['date_format'] = dateFormat

    def setDateColumn(self, dateColumn):
        if not isinstance(dateColumn, string_types):
            raise TypeError("dateColumn格式错误, dateColumn必须是字符串。")
        self['date_column'] = dateColumn

class KSCsvSource(KSBaseSource):
    def __init__(self, 
        filename, 
        dateColumn='datetime', 
        dateFormat="%Y-%m-%d %H:%M:%S", 
        securityColumn=None, 
        priceColumn=None, 
        delimiter=','):
        KSBaseSource.__init__(self)
        self.setDateColumn(dateColumn)
        self.setDateFormat(dateFormat)
        self['type'] = "CSV"
        self['filename'] = filename
        if securityColumn and priceColumn:
            self.tagAsPriceData(securityColumn, priceColumn)
        elif securityColumn:
            self.tagAsSecurityData(securityColumn)
        self.setDelimiter(delimiter)

    def setDelimiter(self, delimiter):
        self['delimiter'] = delimiter
        
class KSMemorySource(KSBaseSource):
    def __init__(self):
        pass
    