# -*- coding: utf-8 -*-

class Riskless(object):
	value = 0.0314
	
	def to_dict(self):
		fields = copy(self.__dict__)
		return fields

	def __repr__(self):
		return self.to_dict().__repr__()

	def __str__(self):
		return self.to_dict().__str__()
