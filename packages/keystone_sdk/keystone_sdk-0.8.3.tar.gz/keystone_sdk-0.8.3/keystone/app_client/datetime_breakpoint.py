# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

class DatetimeBreakpoint(object):
	datetime_breakpoints = {}
	hit_datetime_breakpoint = None

	@classmethod
	def clear(cls):
		cls.datetime_breakpoints = {}
		cls.hit_datetime_breakpoint = None
		
	@classmethod
	def is_break_at_datetime(cls, current_dt):
		sorted_dt = sorted(list(cls.datetime_breakpoints.items()), key=lambda t: t[0])
		break_flag = False
		break_at = None
		for (dt, has_break) in sorted_dt:
			if dt > current_dt:
				break
			if not has_break:
				break_flag = True
				cls.datetime_breakpoints[dt] = True
				break_at = dt
		cls.hit_datetime_breakpoint = break_at
		return break_flag