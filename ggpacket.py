import struct
import time

import ggproto
import packets_pb2

class GGPacket:
	def __init__(self, pid):
		self.pid = pid

	def body(self):
		return ""

	def __str__(self):
		b = self.body()
		header = struct.pack("<II", self.pid, len(b))
		return header + b

def parsePacket(p_type, p_data):
	if (p_type == ggproto.LOGIN105):
		p = packets_pb2.GG105Login()
		p.ParseFromString(p_data)
		return p
	else:
		return None

def readUIN(data):
	return int(data[2:])

class Welcome(GGPacket):
	def __init__(self):
		GGPacket.__init__(self, ggproto.WELCOME)
	def body(self):
		return struct.pack("<I", 0x01020304)

class Login110OK(GGPacket):
	def __init__(self, uin):
		GGPacket.__init__(self, ggproto.LOGIN110_OK)
		self.uin = uin
	def body(self):
		p = packets_pb2.GG110LoginOK()
		p.dummy1 = 1
		p.dummyhash = "nej2844d8d43s2dMNea2584sdf1sf418"
		p.uin = self.uin
		p.server_time = int(time.time())
		return p.SerializeToString()
