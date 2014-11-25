import struct
import time

import ggproto
import packets_pb2

def readUIN(data):
	return int(data[2:])

class GGPacket:
	def __init__(self, pid):
		self.pid = pid

	def body(self):
		return ""

	def __str__(self):
		b = self.body()
		header = struct.pack("<II", self.pid, len(b))
		return header + b

class Notify105Last:
	def ParseFromString(self, data):
		self.blist = []
		while (len(data) > 0):
			(_, uin_len) = struct.unpack("=BB", data[:2])
			data = data[2:]
			uin = data[:uin_len]
			data = data[(uin_len + 1):]
			self.blist.append(int(uin))

class Ping:
	def __init__(self):
		pass

def parsePacket(p_type, p_data):
	if (p_type == ggproto.LOGIN105):
		p = packets_pb2.GG105Login()
		p.ParseFromString(p_data)
		return p
	elif (p_type == ggproto.NOTIFY105_LAST):
		p = Notify105Last()
		p.ParseFromString(p_data)
		return p
	elif (p_type == ggproto.PING):
		return Ping()
	else:
		return None

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

class IMToken(GGPacket):
	def __init__(self):
		GGPacket.__init__(self, ggproto.IMTOKEN)
	def body(self):
		p = packets_pb2.GG110Imtoken()
		p.imtoken = "1234567890123456789012345678901234567890"
		return p.SerializeToString()

class Status80(GGPacket):
	def __init__(self, uin):
		GGPacket.__init__(self, ggproto.STATUS80)
		self.uin = uin
	def body(self):
		return struct.pack("<IIIIhBBII", self.uin, ggproto.STATUS_AVAIL, 0, 0, 0, 255, 0, 0, 0)

class NotifyReply80(GGPacket):
	def __init__(self, blist):
		GGPacket.__init__(self, ggproto.NOTIFY_REPLY80)
		self.blist = blist
	def body(self):
		p = ""
		for uin in self.blist:
			# XXX: copy-pasta
			p = p + struct.pack("<IIIIhBBII", uin, ggproto.STATUS_AVAIL, 0, 0, 0, 255, 0, 0, 0)
		return p

class UserData(GGPacket):
	def __init__(self, blist):
		GGPacket.__init__(self, ggproto.USER_DATA)
		self.blist = blist
	def body(self):
		p = struct.pack("<II", 3, len(self.blist))
		for uin in self.blist:
			p = p + struct.pack("<II", uin, 0)
		return p

class Pong110(GGPacket):
	def __init__(self):
		GGPacket.__init__(self, ggproto.PONG110)
	def body(self):
		p = packets_pb2.GG110Pong()
		p.server_time = int(time.time())
		return p.SerializeToString()
