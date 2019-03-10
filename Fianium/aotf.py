import ctypes


class Aotf:
    def __init__(self, instance_num=0):
        
        __dll = ctypes.CDLL('AotfLibrary.dll')

        __SerialNumber_NIR1 = '1457D78506000022'
        __SerialNumber_NIR2 = '144ED785060000EF'
        
        self.iInstance = instance_num

        self.__handle = ctypes.c_void_p
        
        self.__AotfOpen = __dll.AotfOpen
        self.__AotfOpen.argtypes = [ctypes.c_int]
        self.__AotfOpen.restype = ctypes.c_void_p

        self.__AotfGetInstance = __dll.AotfGetInstance
        self.__AotfGetInstance.argtypes = [ctypes.c_void_p]
        self.__AotfGetInstance.restype = ctypes.c_int

        self.__AotfClose = __dll.AotfClose
        self.__AotfClose.argtypes = [ctypes.c_void_p]
        self.__AotfClose.restype = ctypes.c_bool

        self.__AotfWrite = __dll.AotfWrite
        self.__AotfWrite.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]
        self.__AotfWrite.restype = ctypes.c_bool

        self.__AotfRead = __dll.AotfRead
        # self.__AotfRead.argtypes = [ctypes.c_void_p,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint_p]
        self.__AotfRead.restype = ctypes.c_bool

        self.__AotfIsReadDataAvailable = __dll.AotfIsReadDataAvailable
        self.__AotfIsReadDataAvailable.argtypes = [ctypes.c_void_p]
        self.__AotfIsReadDataAvailable.restype = ctypes.c_bool
        
    def open(self):
        self.__handle = self.__AotfOpen(self.iInstance)
        if self.__handle is not None:
            return True
        else:
            return False
        
    def getinstance(self):
        self.iInstance = self.__AotfGetInstance(self.__handle)

    def close(self):
        if self.__AotfClose(self.__handle):
            return True
        else:
            return False

    def write(self, command):
        command = command + '\r'
        comm = ctypes.create_string_buffer(len(command))
        comm.value = command.encode('ascii')
        if self.__AotfWrite(self.__handle, len(command), comm):
            return True
        else:
            return False

    def read(self):
        BytesRead = ctypes.c_int(0)
        buffersize = 5000
        DataRead = ctypes.create_string_buffer(b'\000'*buffersize)
        
        if self.__AotfRead(self.__handle, ctypes.c_int(buffersize), DataRead, ctypes.byref(BytesRead)):
            DataReceive = DataRead.value.decode('ascii')
            # print(DataReceive)
            # print(len(DataReceive))
            # print(DataRead.value)
            # print(BytesRead.value)
            return DataReceive

    def write_read(self, command):
        self.write(command)
        while not self.isdataready():
            pass
        recv = self.read()
        return recv
        
    def isdataready(self):
        return self.__AotfIsReadDataAvailable(self.__handle)

    def set_channel_frequency(self, channel, freq):
        # 0-200MHz
        comm = "dds f {0} {1}".format(channel, freq)
        self.write(comm)

    def set_channel_amplitude(self, channel, amplitude):
        # 0-16383
        comm = "dds a {0} {1}".format(channel, amplitude)
        self.write(comm)

    def set_wavelength(self, wavelength):
        a3 = -2.15461e-7
        a2 = 6.79466e-4
        a1 = -0.77394
        a0 = 365.39075
        dds_fre = a3*wavelength*wavelength*wavelength+a2*wavelength*wavelength+a1*wavelength+a0
        self.set_channel_frequency(0, dds_fre)


if __name__ == '__main__':
    myaotf = Aotf(0)
    myaotf.open()

    # myaotf.write('BoardId Serial')
    myaotf.write('help')

    while myaotf.isdataready() is False:
        pass

    rec = myaotf.read()

    print(rec)
    myaotf.close()
