# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import abc
import pandas as pd
from datetime import datetime
from six import with_metaclass
from keystone.constant import DATETIME_COLUMN, SID_COLUMN, PRICE_COLUMN

DATAFRAME_KEY = "dataframe"

def unionSecurityData(df, df2):
	if df.empty:
		result = df2
		result.sort(columns=DATETIME_COLUMN, inplace=True)
		result.index = range(len(result))
		return result
	result = []
	comm_columns = df.columns.intersection(df2.columns)
	if comm_columns.size < 2:
		raise ValueError("Internal Error: comm_columns.size < 2")
	elif comm_columns.size == 2: # Column 不冲突，直接union
		# print("Column not conflict")
		result = pd.merge(df,df2, how='outer', on=[DATETIME_COLUMN, SID_COLUMN])
	elif comm_columns.size > 2: # Column可能冲突，先检查冲突，最后concate
		# TODO: 修改成替换而非报错
		# print("Column May conflict")
		conflict = pd.merge(df, df2, how='inner', on=[DATETIME_COLUMN, SID_COLUMN])
		if not conflict.empty:
			raise ValueError("Merge data conflict on " + str(list(comm_columns)))
		# Merge
		result = pd.concat([df, df2], ignore_index=True)

	# Sort
	result.sort(columns=DATETIME_COLUMN, inplace=True)
	result.index = range(len(result))
	return result


def unionSignalData(df, df2):
	if df.empty:
		result = df2
		result.sort(columns=DATETIME_COLUMN, inplace=True)
		result.index = range(len(result))
		return result
	result = []
	comm_columns = df.columns.intersection(df2.columns)
	if comm_columns.size < 1:
		raise ValueError("Internal Error: comm_columns.size < 1")
	elif comm_columns.size == 1: # Column 不冲突，直接union
		# print("Column not conflict")
		result = pd.merge(df,df2, how='outer', on=[DATETIME_COLUMN])
	elif comm_columns.size > 1: # Column可能冲突，先检查冲突，最后concate
		# Need to check confilct
		# print("Column May conflict")
		conflict = pd.merge(df, df2, how='inner', on=[DATETIME_COLUMN])
		if not conflict.empty:
			raise ValueError("Merge data conflict on " + str(list(comm_columns)))
		# Merge
		result = pd.concat([df, df2], ignore_index=True)

	# Sort
	result.sort(columns=DATETIME_COLUMN, inplace=True)
	result.index = range(len(result))
	return result

class KSTableFile(object):
	def __init__(self, path):
		self.path = path

	def readDataframe(self, key=DATAFRAME_KEY):
		return pd.read_hdf(self.path, key)

	def writeDataframe(self, dataframe, key=DATAFRAME_KEY, mode='w'):
		if not isinstance(dataframe, pd.DataFrame):
			raise TypeError("KSTableFile::write_dataframe(): dataframe MUST be an instance of DataFrame")
		dataframe.to_hdf(self.path, key, mode=mode)
