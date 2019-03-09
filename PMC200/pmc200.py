import serial
import time
from config import Config


class PMC200:
	def __init__(self, port='COM5'):
		self.ser = serial.Serial(port, 9600, timeout=1)  # open serial port

	# Every time power on a configuration is required.
	def initialize(self):
		self.to232()
		self.config()
		# todo
		# move to a end and set zero
		# move to half position of the whole range
		# wait
		# Maybe define some macros to facilitate the process
		#

	# activate serial port
	def to232(self):
		cmd = 'TO232\n'.encode("ascii")
		self.ser.write(cmd)

	def config(self):
		# ACTTYP
		act = []
		for item in Config.ACTTYP:
			if item is None:
				act.append('')
			else:
				act.append('"{0}"'.format(item))
		cmd = 'ACTTYP {0},{1}\n'.format(act[0], act[1]).encode("ascii")
		self.ser.write(cmd)

		# ECHO
		cmd = 'ECHO 0\n'.encode("ascii")
		self.ser.write(cmd)

		# todo
		# Unit
		cmd = 'UNITS "{0}","{1}"\n'.format(Config.UNIT[0], Config.UNIT[1]).encode("ascii")
		self.ser.write(cmd)
		#

	def open(self):
		if self.ser.is_open:
			return True
		self.ser.open()
		return True

	def close(self):
		if not self.ser.is_open:
			return True
		self.ser.close()

	def read(self):
		time.sleep(0.5)
		message = self.ser.read(250).decode("ascii")
		print(message)
		return message

	def move(self, channel=1, pos=0):
		if channel == 1:
			cmd = 'MOVE1 {0}\n'.format(pos).encode("ascii")
		elif channel == 2:
			cmd = 'MOVE2 {0}\n'.format(pos).encode("ascii")
		else:
			print("Channel should be either 1 or 2")
			return False
		self.ser.write(cmd)
		return True

	def home(self):
		cmd = 'HOME\n'.encode("ascii")
		self.ser.write(cmd)

	def get_actual_vel(self):
		cmd = 'AVEL?\n'.encode("ascii")
		self.ser.write(cmd)
		self.read()

	def set_acl(self, acl1=2.0, acl2=2.0):
		cmd = 'ACL {0},{1}'.format(acl1, acl2).encode("ascii")
		self.ser.write(cmd)

	def set_vel(self, vel1, vel2):
		cmd = 'VEL {0},{1}'.format(vel1, vel2).encode("ascii")
		self.ser.write(cmd)

	def jog(self, dis1=0.0, dis2=0.0):
		cmd = 'JOG {0},{1}'.format(dis1, dis2).encode("ascii")
		self.ser.write(cmd)

	def get_pos(self):
		cmd = 'POS?'.encode("ascii")
		self.ser.write(cmd)


if __name__ == "__main__":
	pmc200 = PMC200()
	# pmc200.initialize()
	try:
		#pmc200.move(1, -12.5)
		command = b'EVENT?\n'
		pmc200.ser.write(command)     # write a string
		s = pmc200.read()

		for item in Config.PROCESS:
			pmc200.set_acl(item[2], item[2])
			pmc200.set_vel(item[1], item[1])
			pmc200.jog(item[0], item[0])
			print(item)

	finally:
		pmc200.close()
