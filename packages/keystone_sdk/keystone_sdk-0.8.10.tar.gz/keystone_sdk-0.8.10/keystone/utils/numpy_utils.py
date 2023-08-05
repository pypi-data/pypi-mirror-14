# -*- coding: utf-8 -*-

import numpy as np

class nanvar(object):
	def __init__(self, ddof=0):
		self.ddof = ddof
		self.n = 0.0
		self.mean = 0.0
		self.M2 = 0.0
		self.var = np.nan

	@property
	def value(self):
	    return self.var

	def update(self, x):
		if np.isnan(x):
			return
		self.n += 1
		delta = x - self.mean
		self.mean += delta/self.n
		self.M2 += delta*(x - self.mean)

		if self.n > self.ddof:
			self.var = self.M2 / (self.n - self.ddof)

class nanstd(nanvar):
	@property
	def value(self):
	    return np.sqrt(self.var)
	
class nancov(object):
	def __init__(self, ddof=0):
		self.ddof = ddof
		self.n = 0.0
		self.xvar = nanvar(ddof=ddof)
		self.yvar = nanvar(ddof=ddof)
		self.C2 = 0.0
		self.cov = np.full((2,2), np.nan)

	@property
	def value(self):
	    return self.cov

	def update(self, x, y):
		if not np.isnan(x) and not np.isnan(y):
			self.n += 1
			self.C2 += (self.n - 1)/(self.n) * (x - self.xvar.mean) * (y -self.yvar.mean)
			if self.n > self.ddof:
				self.cov[0,1] = self.cov[1,0] = self.C2 / (self.n - self.ddof)
			self.xvar.update(x)
			self.yvar.update(y)
			self.cov[0,0] = self.xvar.value
			self.cov[1,1] = self.yvar.value
