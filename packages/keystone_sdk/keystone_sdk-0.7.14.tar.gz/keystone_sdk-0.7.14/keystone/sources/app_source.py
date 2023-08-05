# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import abc
import pandas as pd
import numpy as np
from datetime import datetime
from six import with_metaclass
from copy import copy

from keystone.sources.kstable import KSTableFile, unionSecurityData, unionSignalData
from keystone.constant import DATETIME_COLUMN, SID_COLUMN, PRICE_COLUMN

# Universe file name
SECURITY_TABLE_FILE = "security.kstable"
SIGNAL_TABLE_FILE = "signal.kstable"
METADATA_FILE = "metadata"

# 
UNIVERSE_BASKET = "basket"
UNIVERSE_SID = "sids"

class KSAppUniverseSource(object):
	def __init__(self, path, basket):
		self.path = path
		self.basket = basket

		self._securityDataFile = path + '/' + SECURITY_TABLE_FILE
		self._signalDataFile = path + '/' + SIGNAL_TABLE_FILE
		self._metaDataFile = path + '/' + METADATA_FILE
		self._metadata = None
		if not self._check():
			raise ValueError(path + " is not a App Universe Data")
		self._loadMetadata()

	def to_dict(self):
		fields = copy(self.__dict__)
		return fields

	def __repr__(self):
		return self.to_dict().__repr__()

	def __str__(self):
		return self.to_dict().__str__()

	def _check(self):
		return True

	def _loadMetadata(self):
		self._metadata = json.load(file(self._metaDataFile))

	def readSecurityDataFrame(self):
		f = KSTableFile(self._securityDataFile)
		# join sids
		sids = []
		for basketName in self.basket:
			if basketName not in self._metadata[UNIVERSE_BASKET]:
				raise ValueError("basket '" + basketName +"' not exist")
			sids = np.union1d(sids, self._metadata[UNIVERSE_BASKET][basketName])
		# filter
		df = f.readDataframe()
		df = df[df[SID_COLUMN].isin(sids)]

		return df

	def readSignalDataFrame(self):
		f = KSTableFile(self._signalDataFile)
		return f.readDataframe()

		