# -*- coding: utf-8 -*-

'''
Session
'''

from __future__ import print_function
import hashlib
import hmac
import logging
import os
import pprint
import random
import uuid
import warnings
import copy
import sys
from datetime import datetime

from keystone.py3compat import PY3, builtin_mod, iteritems, unicode_type, string_types
from keystone.utils.json_utils import extract_dates, date_default

try:
    import cPickle
    pickle = cPickle
except:
    cPickle = None
    import pickle

try:
    # py3
    PICKLE_PROTOCOL = pickle.DEFAULT_PROTOCOL
except AttributeError:
    PICKLE_PROTOCOL = pickle.HIGHEST_PROTOCOL

try:
    # We are using compare_digest to limit the surface of timing attacks
    from hmac import compare_digest
except ImportError:
    # Python < 2.7.7: When digests don't match no feedback is provided,
    # limiting the surface of attack
    def compare_digest(a,b): return a == b

import zmq
from zmq.utils import jsonapi
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

json_packer = lambda obj: jsonapi.dumps(obj, default=date_default,
    ensure_ascii=False, allow_nan=False,
)
json_unpacker = lambda s: jsonapi.loads(s)

pickle_packer = lambda o: pickle.dumps(squash_dates(o), PICKLE_PROTOCOL)
pickle_unpacker = pickle.loads

default_packer = json_packer
default_unpacker = json_unpacker

DELIM = b"<IDS|MSG>"

def msg_header(msg_id, msg_type, username, session):
    date = datetime.now()
    return locals()

def session_default():
    u = unicode_type(uuid.uuid4())
    return u

def extract_header(msg_or_header):
    """Given a message or header, return the header."""
    if not msg_or_header:
        return {}
    try:
        # See if msg_or_header is the entire message.
        h = msg_or_header['header']
    except KeyError:
        try:
            # See if msg_or_header is just the header
            h = msg_or_header['msg_id']
        except KeyError:
            raise
        else:
            h = msg_or_header
    if not isinstance(h, dict):
        h = dict(h)
    return h
'''
Session
header: {msg_id: uuid, message id,
		 msg_type: str, type of message,
		 username: str, username,
		 session: uuid, session id,
		 date: str}
parent_header: dict, header of parent
metadata: dict, metadata 
content: dict, content

The Wire Protocol: [idents, DELIM, signature, header, parent_header, metadata, content]
'''
class Session(object):
	pack = default_packer
	unpack = default_unpacker
	session = session_default()
	username = unicode_type(os.environ.get('USER', 'username'))
	auth = None

	def __init__(self, **kwargs):
		self.pid = os.getpid()
		self.bsession = self.session.encode('ascii')
		self.metadata = None
		self.debug = False
		if 'metadata' in kwargs:
			self.metadata = kwargs['metadata']
		if 'debug' in kwargs:
			self.debug = bool(kwargs['debug'])

	@property
	def msg_id(self):
		"""always return new uuid"""
		return str(uuid.uuid4())

	def msg_header(self, msg_type):
	    return msg_header(self.msg_id, msg_type, self.username, self.session)

	def msg(self, msg_type, header=None, parent=None, content=None, metadata=None):
		"""Return the nested message dict.
		This format is different from what is sent over the wire. The
		serialize/deserialize methods converts this nested message dict to the wire
		format, which is a list of message parts.
		"""
		msg = {}
		header = self.msg_header(msg_type) if header is None else header
		msg['header'] = header
		msg['msg_id'] = header['msg_id']
		msg['msg_type'] = header['msg_type']
		msg['content'] = {} if content is None else content
		msg['parent_header'] = {} if parent is None else parent
		msg['metadata'] = copy.copy(self.metadata)
		if metadata is not None:
		    msg['metadata'].update(metadata)
		return msg

	def sign(self, msg_list):
		"""Sign a message with HMAC digest. If no auth, return b''.
		"""
		if self.auth is None:
		    return b''
		h = self.auth.copy()
		for m in msg_list:
		    h.update(m)
		return str_to_bytes(h.hexdigest())

	def serialize(self, msg, ident=None):
		"""Serialize the message components to bytes."""
		content = msg.get('content', {})
		if content is None:
		    content = self.none
		elif isinstance(content, dict):
		    content = json_packer(content)
		elif isinstance(content, bytes):
		    # content is already packed, as in a relayed message
		    pass
		elif isinstance(content, unicode_type):
		    # should be bytes, but JSON often spits out unicode
		    content = json_packer(content)
		else:
		    raise TypeError("Content incorrect type: %s"%type(content))

		real_message = [json_packer(msg['header']),
						json_packer(msg['parent_header']),
		                json_packer(msg['metadata']),
		                content]

		to_send = []

		if isinstance(ident, list):
		    # accept list of idents
		    to_send.extend(ident)
		elif ident is not None:
		    to_send.append(ident)
		to_send.append(DELIM)

		signature = self.sign(real_message)
		to_send.append(signature)

		to_send.extend(real_message)

		return to_send

	def feed_identities(self, msg_list):
		"""Split the identities from the rest of the message.
		"""
		try:
		    idx = msg_list.index(DELIM)
		except:
		    raise ValueError("DELIM not in msg_list")
		return msg_list[:idx], msg_list[idx+1:]

	def deserialize(self, recv_msg_list, content=True):
		"""Unserialize a msg_list to a nested message dict.
		content : bool (True)
		    Whether to unpack the content dict (True), or leave it packed
		    (False).
		"""
		minlen = 5
		idents, msg_list = self.feed_identities(recv_msg_list)
		message = {}
		if not len(msg_list) >= minlen:
		    raise TypeError("malformed message, must have at least %i elements"%minlen)
		header = json_unpacker(msg_list[1])
		message['header'] = extract_dates(header)
		message['msg_id'] = header['msg_id']
		message['msg_type'] = header['msg_type']
		message['parent_header'] = extract_dates(json_unpacker(msg_list[2]))
		message['metadata'] = json_unpacker(msg_list[3])
		if content:
		    message['content'] = json_unpacker(msg_list[4])
		else:
		    message['content'] = msg_list[4]
		if self.debug:
		    pprint.pprint(message)
		return idents, message

	def send(self, stream, msg_type, content=None, header = None, metadata = None, 
		parent=None, ident=None):
		msg = self.msg(msg_type, content=content, parent=parent,
		                   header=header, metadata=metadata)
		to_send = self.serialize(msg, ident)

		stream.send_multipart(to_send, copy=True)

		# print >>sys.stderr,"Session.send():",
		# print >>sys.stderr, to_send
		if self.debug:
		    pprint.pprint(msg)
		    pprint.pprint(to_send)
		    pprint.pprint(buffers)

		return msg

	def recv(self, socket, mode=zmq.NOBLOCK, content=True):
		"""Receive and unpack a message."""
		if isinstance(socket, ZMQStream):
		    socket = socket.socket
		try:
		    msg_list = socket.recv_multipart(mode, copy=True)
		except zmq.ZMQError as e:
		    if e.errno == zmq.EAGAIN:
		        # We can convert EAGAIN to None as we know in this case
		        # recv_multipart won't return None.
		        return None,None
		    else:
		        raise
		try:
		    return self.deserialize(msg_list, content=content)
		except Exception as e:
		    # TODO: handle it
		    raise e

