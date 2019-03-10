import serial
import time


class Powermeter:
    def __init__(self, port='COM4', baudrate=19200):
        self.port = port
        self.baudrate = baudrate
        self.ser = serial.Serial(self.port, self.baudrate)

    def open(self):
        if self.ser.isOpen() is False:
            self.ser.open()

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

    def write_read(self, command):
        self.write(command)
        time.sleep(0.5)
        recv = self.read()
        return recv.strip()

    def get_power(self):
        data = self.write_read('D?')
        return float(data)

    def set_wavelength(self, wavelength):
        wavelength = int(wavelength)
        self.write('W{0}'.format(wavelength))

        
if __name__ == "__main__":
    pm = Powermeter(port="COM4")
    pm.open()
    for index in range(100):
        print(pm.write_read("D?"))
    pm.close()
