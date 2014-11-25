import struct

class GGPacket:
	def __init__(self, pid):
		self.pid = pid

	def body(self):
		return ""

	def __str__(self):
		b = self.body()
		header = struct.pack("<II", self.pid, len(b))
		return header + b

class Welcome(GGPacket):
	def __init__(self):
		GGPacket.__init__(self, 0x0001)
	def body(self):
		return struct.pack("<I", 0x01020304)
