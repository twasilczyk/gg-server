#!/usr/bin/env python

import SocketServer
import time
import struct
import ggpacket

class GGServer(SocketServer.BaseRequestHandler):
	def gg_recv_packet(self):
		(p_type, p_len) = struct.unpack("<II", self.request.recv(8))
		p_data = self.request.recv(p_len)

	def handle(self):
		print "client"
		self.request.sendall(str(ggpacket.Welcome()))
		self.gg_recv_packet()
		# TODO: send LOGIN105_OK
		time.sleep(5)

server = SocketServer.TCPServer(('0.0.0.0', 8074), GGServer)
server.serve_forever()
