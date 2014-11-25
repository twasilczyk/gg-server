#!/usr/bin/env python

import SocketServer
import time
import struct
import ggpacket

import packets_pb2

class GGServer(SocketServer.BaseRequestHandler):
	def setup(self):
		self.is_valid = True

	def recvExactly(self, length):
		total = ""
		retry = False
		while (len(total) < length):
			got = self.request.recv(length - len(total))
			if (len(got) == 0):
				if retry:
					return None
				else:
					retry = True
					time.sleep(1)
			else:
				retry = False
			total = total + got
		return total

	def recvPacket(self):
		data = self.recvExactly(8)
		if (not data):
			self.is_valid = False
			return None
		(p_type, p_len) = struct.unpack("<II", data)
		if (p_len == 0):
			return ggpacket.parsePacket(p_type, "")
		p_data = self.recvExactly(p_len)
		if (not p_data):
			self.is_valid = False
			return None
		return ggpacket.parsePacket(p_type, p_data)

	def send(self, p):
		self.request.sendall(str(p))

	def handle(self):
		print "new client connected"
		self.send(ggpacket.Welcome())
		while self.is_valid:
			p = self.recvPacket()
			if (isinstance(p, packets_pb2.GG105Login)):
				self.send(ggpacket.Login110OK(ggpacket.readUIN(p.uin)))
			elif (isinstance(p, ggpacket.Notify105Last)):
				self.send(ggpacket.NotifyReply80(p.blist))
		print "client disconnected"

server = SocketServer.TCPServer(('0.0.0.0', 8074), GGServer)
server.serve_forever()
