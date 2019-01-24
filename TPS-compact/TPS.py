import serial
import time


class TPS:
    def __init__(self, com=None):
        self.ser = serial.Serial(com, 9600, timeout=1)

    def write(self, win='163', data='000000'):
        stx = 0x02
        addr = 0x80
        com = 0x31
        etx = 0x03
        _win = list(map(lambda x: ord(x), win))
        _data = list(map(lambda x: ord(x), data))
        _cmd = [stx, addr]+_win+[com]+_data+[etx]
        crc = 0
        for item in _cmd[1:]:
            crc ^= item
        crc = crc % 256
        _crc = list()
        _crc.append(hex(crc//16).encode().upper()[2])
        _crc.append(hex(crc % 16).encode().upper()[2])
        cmd = _cmd+_crc
        print(list(map(hex, cmd)))
        writed_num = self.ser.write(cmd)
        #print(f"write: {writed_num}")
        time.sleep(0.2)
        n = self.ser.in_waiting
        ret = self.ser.read(n)
        #print(f"read {n}")
        p = []
        for item in ret:
            p.append(hex(item))
        print(p)
        _results = ret[-4]
        results = hex(_results)
        print(results)
        if _results == 0x06:
            return True
        else:
            return False

    def read(self, win, data_type):
        if data_type == 'N':
            n_results = 6
        elif data_type == 'A':
            n_results = 10
        elif data_type == 'L':
            n_results = 1
        else:
            return False
        stx = 0x02
        addr = 0x80
        com = 0x30
        etx = 0x03
        _win = list(map(lambda x: ord(x), win))
        _cmd = [stx, addr] + _win + [com, etx]
        crc = 0
        for item in _cmd[1:]:
            crc ^= item
        crc = crc % 256
        _crc = list()
        _crc.append(hex(crc // 16).encode().upper()[2])
        _crc.append(hex(crc % 16).encode().upper()[2])
        cmd = _cmd + _crc
        # print(list(map(hex, cmd)))
        writed_num = self.ser.write(cmd)
        # print(f"write: {writed_num}")
        time.sleep(0.2)
        n = self.ser.in_waiting
        ret = self.ser.read(n)
        # print(f"read {n}")
        p = []
        for item in ret:
            p.append(hex(item))
        print(p)
        _results = ret[-(n_results + 3):(-3)]
        results = ""
        for item in _results:
            results += chr(item)
        print(results)
        return results

    def close(self):
        self.ser.close()
        print(f"Port {self.ser.name} Closed")

    def set_pressure_unit(self, unit):
        win = '163'
        if unit == "mBar":
            data = "000000"
        elif unit == "Pa":
            data = "000001"
        elif unit == "Torr":
            data = "000002"
        else:
            return False
        return self.write(win, data)

    def get_pressure_unit(self):
        self.read("163", 'N')

    def get_controller_air_temperature(self):
        return int(self.read("216", 'N'))

    def set_stop_speed_reading(self, data):
        self.write("167", data)

    def get_stop_speed_reading(self):
        return self.read("167", 'L')  # There should be a data type error in the manual

    def get_rotation_frequency(self):
        return int(self.read("226", 'N'))

    def set_remote_mode(self, data):
        self.write("008", data)

    def get_remote_mode(self):
        return int(self.read("008", 'L'))

    def set_start(self, data):
        return self.write("000", data)

    def get_start(self):
        return int(self.read("000", 'L'))

    @property
    def is_started(self):
        return bool(int(self.get_start()))

    def get_pressure(self):
        return float(self.read("224", 'A'))


if __name__ == "__main__":
    tps = TPS('COM4')
    try:
        # tps.get_pressure_unit()
        # tps.set_pressure_unit("mBar")
        # tps.get_pressure_unit()
        # tps.get_controller_air_temperature()
        # tps.get_remote_mode()
        # tps.set_remote_mode('0')
        # if tps.get_remote_mode() == 0:
        #     if tps.is_started:
        #         tps.set_start('0')
        # tps.set_stop_speed_reading('1')
        # tps.get_stop_speed_reading()
        # tps.set_start('1')
        print(tps.get_rotation_frequency())
        print(tps.get_pressure())

    finally:
        tps.close()
