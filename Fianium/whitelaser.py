import serial
import time


class WhiteLaser:
    def __init__(self, port='COM3', baudrate=19200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port, self.baudrate)

        self.back_ref_alarm = 0
        self.max_dac = 0

    def open(self):
        if self.ser.isOpen() is False:
            self.ser.open()

    def initialise(self):
        # minimize the information
        self.write_read("x=2")
        self.back_ref_alarm = self.get('l')
        self.max_dac = self.get_max_dac()

    def write(self, command):
        comm = command + '\n'
        self.ser.write(comm.encode('ascii'))

    def read(self):
        recv = ''
        count = self.ser.inWaiting()
        recv = recv + self.ser.read(count).decode('ascii')
        return recv

    def close(self):
        self.ser.close()

    def parse(self, recv):
        parsed = recv.split(',',1)
        # print("Original:")
        # print(recv)
        # print("Parsed: ")
        # print(parsed[1])
        try:
            return int(parsed[1])
        except:
            return float(parsed[1])

    def write_read(self, command):
        self.write(command)
        time.sleep(1)
        recv = self.read()
        return recv.strip()

    def set(self, setting, value):
        command = setting + '=' + str(value)
        return self.write_read(command)

    def get(self, setting):
        command = setting + '?'
        parsed = self.parse(self.write_read(command))
        return parsed

    def check_ok(self):
        if self.get('a') != 0:
            return False
        else:
            return True

    def set_repetition_rate(self,frequency):
        # check the on/off status of the laser
        # before you change the repetition rate
        self.set('r', frequency)
        self.max_dac = self.get_max_dac()

    def get_repetition_rate(self):
        return self.get('r')

    def set_power(self, power):
        if not self.check_on():
            return
        dac_value = int(self.max_dac*power/100)
        self.set('q',dac_value)

    def get_power(self):
        return int(self.get('q')/self.max_dac*100)

    def get_max_dac(self):
        return self.get('s')
        
    def check_on(self):
        if self.get('key') !=0:
            return True
        else:
            return False

    def turn_on(self):
        if self.check_on():
            return
        if not self.check_hwkey():
            return False
        self.set('key',1)
        return self.check_on()

    def turn_off(self):
        if not self.check_on():
            return
        self.set('key',0)
        return not self.check_on()

    def check_hwkey(self):
        if self.get('hwkey') == 0:
            return False
        else:
            return True


if __name__ == "__main__":
    wl = WhiteLaser()
    wl.open()
    wl.initialise()
    print(wl.write_read("v?"))
    #wl.close()
