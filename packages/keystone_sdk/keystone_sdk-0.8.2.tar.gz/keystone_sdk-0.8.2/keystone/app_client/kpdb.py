# -*- coding: utf-8 -*-

from __future__ import print_function
import random
import zmq
import sys
import time
import json
import importlib
import imp
import abc
import pytz
from pdb import Pdb
from datetime import datetime
from six import with_metaclass
from zmq.eventloop import ioloop, zmqstream
from zmq.eventloop.zmqstream import ZMQStream
import linecache
import multiprocessing

from keystone.utils import zmq_utils 
from keystone.utils.json_utils import json_clean, UTC_TIMESTAMP
from keystone.app_client.datetime_breakpoint import DatetimeBreakpoint
from keystone.py3compat import safe_unicode, PY3
from keystone.universe import KSUniverse as Universe

if not PY3:
	from Queue import Queue
	import thread as _thread
else:
	from queue import Queue
	import _thread


KPDB_NOTIFY_REACH_BREAKPOINT = "kpdb_notify_reach_breakpoint"
KPDB_SET_BREAKPOINT_REPLY = "kpdb_set_breakpoint_reply"

KPDB_MSG_TYPE = [KPDB_NOTIFY_REACH_BREAKPOINT, KPDB_SET_BREAKPOINT_REPLY]

class KPdb(Pdb):
	def __init__(self, 
		filename,
		session, 
		notify_url, 
		syn_url, 
		control_url,
		datetime_break_func=None,
		datetime_break_cond=None,
		completekey='tab', stdin=None, stdout=None, skip=None):
		Pdb.__init__(self, completekey, stdin, stdout, skip)
		self.filename = filename
		self.stop_flag = False
		self.pause_flag = False
		self.lock = multiprocessing.Lock() 
		self.session = session
		self.init_notify_sock(notify_url, syn_url)
		self.init_control_sock(control_url)

		# set datetime break condition
		self.datetime_break_func = datetime_break_func
		self.datetime_break_cond = datetime_break_cond
		self.current_time_func = lambda: Universe.time
		if self.datetime_break_func is not None:
			self._break_at_function(self.datetime_break_func, cond=self.datetime_break_cond)

	def init_notify_sock(self, notify_url, syn_url):
		self.notify_socket = zmq_utils.create_publisher_socket(notify_url, syn_url)

	def init_control_sock(self, control_url):
		# print("control_url: %s"%(control_url))
		control_socket = zmq.Context().socket(zmq.ROUTER)
		control_socket.bind(control_url)
		self.control_socket = control_socket
		# 改掉，不能再这里启动线程
		_thread.start_new_thread(self.handle_control_message, (control_socket,))

	def handle_control_message(self, socket, mode=zmq.NOBLOCK, content=True):
		"""Receive and unpack a message."""
		# print("control_thread started")
		if isinstance(socket, ZMQStream):
			socket = socket.socket
		while 1:
			try:
			    msg_list = socket.recv_multipart(mode, copy=True)
			except zmq.ZMQError as e:
				if e.errno == zmq.EAGAIN:
					# We can convert EAGAIN to None as we know in this case
					# recv_multipart won't return None.
					continue
				else:
					raise
			try:
				# print("==========================")
				# print("recieve control message")
				# print(msg_list)
				ident, reply = self.session.deserialize(msg_list, content=content)
				# print("*********ident(%s), recieve %s"%(ident, reply), file=sys.stderr)
				self.set_pause()
				self.session.send(socket, safe_unicode('stop_reply'), content = {'result': 0}, ident = ident)
			except Exception as e:
				# TODO: handle it
				raise e

	def notify_frontend(self, msg_type, content):
		assert msg_type in KPDB_MSG_TYPE

		content = json_clean(content)
		msg = self.session.send(self.notify_socket, safe_unicode(msg_type), content = content, ident = b'stream.kpdb_notify')

	def construct_notify_message(self, frame):
		fname = self.canonic(frame.f_code.co_filename)
		lineno = frame.f_lineno
		if DatetimeBreakpoint.hit_datetime_breakpoint is None:
			content = json_clean(dict(type='line_breakpoint', filename=fname, lineno=lineno))
		else:
			content = json_clean(dict(
				type='datetime_breakpoint', 
				datetime=DatetimeBreakpoint.hit_datetime_breakpoint, 
				filename=fname, 
				lineno=lineno,
				datetime_format=UTC_TIMESTAMP))
		return content

	def trace_dispatch(self, frame, event, arg):
		with self.lock:
			self.stop_flag = False
		return Pdb.trace_dispatch(self, frame, event, arg)

	def forget(self):
		DatetimeBreakpoint.hit_datetime_breakpoint = None
		Pdb.forget(self)

	def set_pause(self):
		with self.lock:
			# print("self.stop_flag = %d"%(self.stop_flag), file=sys.stderr)
			if not self.stop_flag:
				self.pause_flag = True

	# overide step_here,用于限制用户只能停留在当前文件中
	def stop_here(self, frame):
		fname = self.canonic(frame.f_code.co_filename)
		# print(self.frame_returning)
		# print(self.stopframe)
		# print(self.botframe)
		# print(self.stoplineno)
		# if self.botframe is not None:
		# 	print(self.botframe.f_code)
		if fname != self.filename:
			return False
		with self.lock:
			if self.stop_flag:
				return True
			elif self.pause_flag:
				self.stop_flag = True
				self.pause_flag = False # reset pause flag
				# print("func stop_here, pause_flag=%d, file=%s, code=%s"%(self.pause_flag, fname, frame.f_code), file=sys.stderr)
				return True
			elif Pdb.stop_here(self,frame):
				self.stop_flag = True
				return True
			else:
				return False
		
	def user_return(self, frame, return_value):
		# construct notify message
		# content = self.construct_notify_message(frame)
		# notify frontend
		# self.notify_frontend(msg_type=KPDB_NOTIFY_REACH_BREAKPOINT, content=content)
		Pdb.user_return(self, frame, return_value)
		
	def user_call(self, frame, argument_list):
		# construct notify message
		# content = self.construct_notify_message(frame)
		# notify frontend
		# self.notify_frontend(msg_type=KPDB_NOTIFY_REACH_BREAKPOINT, content=content)
		Pdb.user_call(self, frame, argument_list)

	def user_line(self, frame):
		# construct notify message
		content = self.construct_notify_message(frame)
		# notify frontend
		self.notify_frontend(msg_type=KPDB_NOTIFY_REACH_BREAKPOINT, content=content)
		# call Pdb.user_line
		Pdb.user_line(self, frame)

	''' custom clear_all function without interaction with user '''
	def do_clear_all(self, arg):
		self.clear_all_breaks()
		DatetimeBreakpoint.clear()
		# restore datetime break condition
		if self.datetime_break_func is not None:
			self._break_at_function(self.datetime_break_func, cond=self.datetime_break_cond)

	''' override original do_clear function '''
	def do_clear(self, arg):
		if not arg:
			DatetimeBreakpoint.clear()
		Pdb.do_clear(self,arg)
		# restore datetime break condition
		if self.datetime_break_func is not None:
			self._break_at_function(self.datetime_break_func, cond=self.datetime_break_cond)

	def do_break_line(self, arg, temporary = 0):
		filename = None
		lineno = None
		colon = arg.rfind(':')
		if colon >= 0:
			filename = arg[:colon].rstrip()
			arg = arg[colon+1:].lstrip()
			try:
				lineno = int(arg)
				err = self._break_at_line(filename, lineno, temporary)
				if err:
					pass
					# print >>sys.stderr, err
					# return
			except ValueError as msg:
				print('***(KPdb) Bad lineno:', arg, file=sys.stderr)
				return
		else:
			print("***(KPdb) Bad arguments: ", arg, file=sys.stderr)

	def do_unbreak_line(self, arg, temporary = 0):
		filename = None
		lineno = None
		colon = arg.rfind(':')
		if colon >= 0:
			filename = arg[:colon].rstrip()
			arg = arg[colon+1:].lstrip()
			try:
				lineno = int(arg)
				err = self.clear_break(filename, lineno)
				if err:
					pass
					# print >>sys.stderr, err
					# return
			except ValueError as msg:
				print('***(KPdb) Bad lineno:', arg, file=sys.stderr)
				return
		else:
			print("***(KPdb) Bad arguments: ", arg, file=sys.stderr)


	def do_break_datetime(self, arg, temporary = 0):
		# print >>sys.stdout, "this is KPdb break_datetime"
		# print >>sys.stdout, arg
		try:
			timestamps = arg.split(',')
			for ts in timestamps:
				dt = datetime.utcfromtimestamp(float(ts))
				current_dt = None
				if self.current_time_func is not None:
					current_dt = self.current_time_func()

				if current_dt is None or dt > current_dt:
					DatetimeBreakpoint.datetime_breakpoints[dt] = False
				# print >>sys.stdout, "break point: ",
				# print >>sys.stdout, dt
		except Exception as e:
			print(e, file=sys.stderr)

	def do_unbreak_datetime(self, arg):
		# print >>sys.stdout, "this is KPdb unbreak_datetime"
		# print >>sys.stdout, arg
		try:
			timestamps = arg.split(',')
			for ts in timestamps:
				dt = datetime.utcfromtimestamp(float(ts))
				if dt in DatetimeBreakpoint.datetime_breakpoints:
					del DatetimeBreakpoint.datetime_breakpoints[dt]
		except Exception as e:
			print(e, file=sys.stderr) 

	def _break_at_line(self, filename, lineno, temporary = 0, cond = None):
		funcname = None
		filename = filename.rstrip()
		f = self.lookupmodule(filename)
		if not f:
			return '***(KPdb) ' + repr(filename) + 'not found'
		else:
		    filename = f
		try:
		    lineno = int(lineno)
		except ValueError as msg:
		    return '***(KPdb) Bad lineno:' + str(lineno)

		# now check line
		err = self._checkline(filename, lineno)
		if err:
			return '***(KPdb) ' + err
		# now set the break point
		err = self.set_break(filename, lineno, temporary, cond, funcname)
		if err: 
			return '***(KPdb) ' + err
		# bp = self.get_breaks(filename, line)[-1]
		# print >>self.stdout, "Breakpoint %d at %s:%d" % (bp.number,
		#                                                  bp.file,
		#                                                  bp.line)

	def _break_at_function(self, arg, temporary = 0, cond = None):
		try:
		    func = eval(arg, self.curframe.f_globals, self.curframe_locals)
		except:
		    func = arg
		try:
			if hasattr(func, 'im_func'):
				if PY3:
					func = func.__func__
				else:
					func = func.im_func
			if PY3:
				code = func.__code__
			else:
				code = func.func_code
			#use co_name to identify the bkpt (function names
			#could be aliased, but co_name is invariant)
			funcname = code.co_name
			lineno = code.co_firstlineno
			filename = code.co_filename
		except:
		    # last thing to try
		    (ok, filename, ln) = self.lineinfo(arg)
		    if not ok:
		        return '***(KPdb) The specified object' + repr(arg) + 'is not a function or was not found along sys.path.'

		    funcname = ok # ok contains a function name
		    lineno = int(ln)

		# now check line
		err = self._checkline(filename, lineno)
		if err:
			return '***(KPdb) ' + err
		# now set the break point
		err = self.set_break(filename, lineno, temporary, cond, funcname)
		if err: 
			return '***(KPdb) ' + err

	def _checkline(self, filename, lineno):
		# Check whether specified line seems to be executable.
		globs = self.curframe.f_globals if hasattr(self, 'curframe') and self.curframe is not None else None
		line = linecache.getline(filename, lineno, globs)
		if not line:
		    return '***(KPdb) End of file'
		line = line.strip()
		# Don't allow setting breakpoint at a blank line
		if (not line or (line[0] == '#') or
		     (line[:3] == '"""') or line[:3] == "'''"):
		    return '***(KPdb) Blank or comment'



