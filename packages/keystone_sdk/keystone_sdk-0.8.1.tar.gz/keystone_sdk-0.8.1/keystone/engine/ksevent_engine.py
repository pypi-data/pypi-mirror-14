
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import abc
import pandas as pd
import numpy as np
from datetime import datetime
from six import with_metaclass

from collections import Iterable
from keystone.sources.kstable import KSTableFile, unionSecurityData, unionSignalData
from keystone.sources.app_source import KSAppUniverseSource

from keystone.py3compat import PY3, builtin_mod, iteritems, unicode_type, string_types
from keystone.constant import DATETIME_COLUMN, SID_COLUMN, PRICE_COLUMN, SIGNAL_DATA_SID_COLUMNS

class KSDataEvent(object):
	def __init__(self, dt, data):
		self.dt = dt
		self.data = data
		self.data.index = data[SID_COLUMN]

	def time(self):
		return self.dt

	def securities(self):
		return self.data[SID_COLUMN].unique()

	def query(self, ids, fieldname):
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

		if fieldname not in self.data.columns:
			raise ValueError("'" + fieldname + "' not exist")
		## old version
		# ids = np.unique(ids)
		# df = self.data
		# ret = df[df[SID_COLUMN].isin(ids)][fieldname]
		# if len(ids) == 1:
		# 	if ret.empty:
		# 		ret = np.nan
		# 	else:
		# 		ret = ret.squeeze()
		
		ret = pd.Series(ids, index=ids, copy=True)
		for sid in ids:
			if sid not in self.data.index:
				raise KeyError("不存在id为\'" + sid +"\'的\'" + fieldname + "\'值。")
			ret[sid] = self.data.ix[sid, fieldname]
		return ret.squeeze()

	def getAllData(self):
		return {}

class KSEventEngine(object):
	def __init__(self):
		self.data = pd.DataFrame()

	def addSource(self, source):
		'''
		config: List of basket name
		'''
		if not isinstance(source, KSAppUniverseSource):
			raise TypeError("source必须为'KSAppUniverseSource'对象。")

		df = source.readSecurityDataFrame()
		self.data = unionSecurityData(self.data, df)

		df = source.readSignalDataFrame()
		if df.empty == False:
			df.insert(len(df.columns), SID_COLUMN, SIGNAL_DATA_SID_COLUMNS)
			self.data = unionSecurityData(self.data, df)

	@property
	def dataEvent(self):
		for (dt, data) in self.data.groupby(DATETIME_COLUMN):
			# if isinstance(dt, np.int64):
			# 	ns = 1e-9
			# 	dt = datetime.utcfromtimestamp(dt * ns)
			yield KSDataEvent(dt, data)
