import serial
import time
from config import Config


class PMC200:
	def __init__(self, port='COM5'):
		self.ser = serial.Serial(port, 9600, timeout=1)  # open serial port
		print(self.ser.name)  # check which port was really used
		print(self.ser.bytesize)
		print(self.ser.baudrate)
		print(self.ser.parity)
		print(self.ser.stopbits)

	# Every time power on a configuration is required.
	def initialize(self):
		self.to232()
		self.config()

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

		# todo

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


if __name__ == "__main__":
	pmc200 = PMC200()
	pmc200.initialize()
	try:
		command = b'*IDN?\n'
		pmc200.ser.write(command)     # write a string
		s = pmc200.read()
	finally:
		pmc200.close()
