import serial
import time
from config import Config


class PMC200:
	def __init__(self, port='COM5'):
		self.ser = serial.Serial(port, 9600, timeout=1)  # open serial port

	# Every time power on a configuration is required.
	def initialize(self, has_zero=True):
		if not has_zero:
			self.to232()
			self.config()
			# move to a end and set zero
			pmc200.goto_end(-1)
			# ZERO
			pmc200.zero()
		# move to half position of the whole range
		pmc200.move(0, Config.CENTER_POS)
		# wait
		pmc200.wait_complete(Config.CENTER_POS)

		# ToDo
		# Maybe define some macros to facilitate the process
		#

	# activate serial port
	def to232(self):
		cmd = 'TO232\n'.encode("ascii")
		self.ser.write(cmd)

	def config(self):
		# ECHO off
		# need to turn off the echo off first, otherwise the parse
		# in the follow will fail.
		cmd = 'ECHO 0\n'.encode("ascii")
		self.ser.write(cmd)
		time.sleep(2)
		# clear the message from PMC200 before disabling ECHO
		self.ser.flushInput()

		# ACTTYP
		act = []
		for act_type in Config.ACTTYP:
			if act_type is None:
				act.append('')
			else:
				act.append('"{0}"'.format(act_type))
		cmd = 'ACTTYP {0},{1}\n'.format(act[0], act[1]).encode("ascii")
		self.ser.write(cmd)

		# Unit
		cmd = 'UNITS "{0}","{1}"\n'.format(Config.UNIT[0], Config.UNIT[1]).encode("ascii")
		self.ser.write(cmd)
		# todo

	def reset(self):
		cmd = '*RST\n'.encode("ascii")
		self.ser.write(cmd)

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
		time.sleep(0.1)
		message = self.ser.read(250).decode("ascii")
		return message

	# axis = 0 means move both axises
	def move(self, axis: int = 0, pos: float = 0.0):
		cmd_list = ['MOVE', 'MOVE1', "MOVE2"]
		if 0 < axis < 3:
			cmd = (cmd_list[axis]+' {0}\n').format(pos).encode("ascii")
		elif axis == 0:
			cmd = (cmd_list[axis]+' {0},{0}\n').format(pos).encode("ascii")
		else:
			return
		self.ser.write(cmd)

	def home(self):
		cmd = 'HOME\n'.encode("ascii")
		self.ser.write(cmd)

	def zero(self):
		cmd = 'ZERO\n'.encode("ascii")
		self.ser.write(cmd)

	# todo this function seems to not work
	def get_actual_vel(self):
		cmd = 'AVEL?\n'.encode("ascii")
		self.ser.write(cmd)
		print(self.read())

	def set_acl(self, acl1: float = 2.0, acl2: float = 2.0):
		cmd = 'ACL {0},{1}\n'.format(acl1, acl2).encode("ascii")
		self.ser.write(cmd)

	def set_vel(self, vel1: float, vel2: float):
		cmd = 'VEL {0},{1}\n'.format(vel1, vel2).encode("ascii")
		self.ser.write(cmd)

	def jog(self, dis1: float = 0.0, dis2: float = 0.0):
		cmd = 'JOG {0},{1}\n'.format(dis1, dis2).encode("ascii")
		self.ser.write(cmd)

	def get_pos(self) -> list:
		pos = [0.0, 0.0]
		cmd = 'POS?\n'.encode("ascii")
		self.ser.write(cmd)
		result = self.read()
		p = result.split(',')
		pos[0], pos[1] = float(p[0]), float(p[1])
		return pos

	def run(self, vel1: float = 0.0, vel2: float = 0.0):
		cmd = 'RUN {0},{1}\n'.format(vel1, vel2).encode("ascii")
		self.ser.write(cmd)

	# axis = 0 means stop both axises
	def stop(self, axis: int = 0):
		cmd_list = ["STOP", "STOP1", "STOP2"]
		cmd = (cmd_list[axis]+'\n').encode("ascii")
		self.ser.write(cmd)

	def read_limit(self) -> int:
		cmd = 'EVENT?\n'.encode("ascii")
		self.ser.write(cmd)
		return int(self.read())

	@staticmethod
	def check_limit(event_flag: int) -> list:
		result = [0, 0]
		if event_flag & 0x01:
			result[0] = 1
		elif event_flag & 0x02:
			result[0] = -1
		if event_flag & 0x04:
			result[1] = 1
		elif event_flag & 0x08:
			result[1] = -1
		return result

	def wait_complete(self, target_pos: float):
		count = 0
		pos = [0.0, 0.0]
		while abs(pos[0] - target_pos) > 0.001 or abs(pos[1] - target_pos) > 0.001:
			pos = self.get_pos()
			print(count, pos)
			count += 1

	# end_direction could be +1 or -1
	def goto_end(self, end_direction: int = 1):
		vel = end_direction * 40
		self.run(vel, vel)  # if vel > 0 direction must be +1 other wise -1

		count = 0
		reach_end_1, reach_end_2 = 0, 0
		# wait until both reach end
		while (reach_end_1 + reach_end_2) < 2:
			flag = self.read_limit()
			end_flag = self.check_limit(flag)
			if end_flag[0] == end_direction:
				reach_end_1 = 1
			if end_flag[1] == end_direction:
				reach_end_2 = 1
			count += 1
			print("count: {0}, end1: {1} end2: {2}".format(count, reach_end_1, reach_end_2))
		print("Reach End!")


if __name__ == "__main__":
	# debug variable
	zeroed = True

	pmc200 = PMC200(port='COM5')
	# pmc200.initialize(has_zero=zeroed)
	try:
		# wait for command to start
		input("Press enter to continue if ready!\n")
		# Task
		target_pos = Config.CENTER_POS
		for item in Config.PROCESS:
			pmc200.set_acl(item[2], item[2])
			pmc200.set_vel(item[1], item[1])
			pmc200.jog(-item[0], -item[0])
			target_pos = target_pos - item[0]
			pmc200.wait_complete(target_pos)
			print(item)
		print("Completed!")
		# check command
		# command = b'EVENT?\n'
		# pmc200.ser.write(command)     # write a string
		# s = pmc200.read()
	finally:
		pmc200.close()
