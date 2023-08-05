# -*- coding: utf-8 -*-

from __future__ import print_function
from datetime import datetime
import pprint
import sys
import time
import zmq

from keystone.api import keystone_class, api_method
from keystone.coordinator import KSObserver, KSCoordinator
from keystone.app_client.session import Session
from keystone.order import KSOrderEventType
from keystone.py3compat import PY3, builtin_mod, iteritems
from keystone.utils.json_utils import json_clean, UTC_TIMESTAMP
import keystone.utils.zmq_utils as zmq_utils

if not PY3:
	from Queue import Queue
	import thread as _thread
else:
	from queue import Queue
	import _thread

class KSDrain(KSObserver):
	class DrainThreadStop:
		pass
	session = Session()
	context = zmq.Context()
	send_data = False
	def __init__(self, 
		strategy_manager, 
		drain_url='tcp://127.0.0.1:55558', 
		syn_url='tcp://127.0.0.1:55559', 
		debug=False):
		self.strategy_manager = strategy_manager
		self.drain_url = drain_url
		self.syn_url = syn_url
		self.debug = debug
		self.orders = []
		self.buffer = Queue()
		self.sock = zmq_utils.create_publisher_socket(self.drain_url, self.syn_url)

	def msg(self, dt):
		msg = {
		'datetime': dt,
		'portfolio_value': self.strategy_manager.portfolio.value(),
		'cash': self.strategy_manager.portfolio.cash(),
		'positions': [pos.to_dict() for pos in self.strategy_manager.portfolio.positions()],
		'orders': [order.to_dict() for order in self.orders],
		}
		msg.update(self.strategy_manager.analyzers[0].value())
		return msg

	def onDataEvent(self, dataEvent):
		# generate message
		msg = self.msg(dataEvent.time())
		if self.send_data:
			msg['data'] = dataEvent.getAllData()
		msg = json_clean(msg, datetime_format = UTC_TIMESTAMP)
		# clear orders
		self.orders = []
		# trigger send method
		self.send(msg)

	def onOrderEvent(self, orderEvent):
	    if orderEvent.type != KSOrderEventType.ACCEPTED and orderEvent.type != KSOrderEventType.CANCELLED:
	    	self.orders.append(orderEvent.txn)

	def send(self, msg):
		# self.buffer.put(msg, block = True)
		self.session.send(self.sock, 'drain', content = msg, ident = b'stream.drain')

	def sendMessage(self):
		count = 1
		while True:
			message = self.buffer.get(block = True)
			if isinstance(message, self.DrainThreadStop):
				return
			self.session.send(self.sock, 'drain', content = message, ident = b'stream.drain')

	def start(self):
		return
		_thread.start_new_thread(self.sendMessage, ())

	def wait(self):
		self.buffer.put(self.DrainThreadStop())
