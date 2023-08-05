# -*- coding: utf-8 -*-

import zmq
import sys

def create_publisher_socket(publisher_url, syn_url = None, SUBSCRIBERS_EXPECTED = 1):
	context = zmq.Context()

	# Socket to talk to clients
	publisher = context.socket(zmq.PUB)
	# set SNDHWM, so we don't drop messages for slow subscribers
	# publisher.sndhwm = 1100000
	publisher.bind(publisher_url)

	if syn_url is not None:
		# Socket to receive signals
		syncservice = context.socket(zmq.REP)
		syncservice.bind(syn_url)

		# Get synchronization from subscribers
		subscribers = 0
		while subscribers < SUBSCRIBERS_EXPECTED:
		    # wait for synchronization request
		    msg = syncservice.recv()
		    # send synchronization reply
		    syncservice.send(b'')
		    subscribers += 1
		    # print >>sys.stderr,("+1 subscriber (%i/%i)" % (subscribers, SUBSCRIBERS_EXPECTED))

		# Now broadcast exactly 1M updates followed by END
		# for i in range(1000000):
		#     publisher.send(b'Rhubarb')

		# publisher.send(b'END')
		syncservice.close()
	return publisher