import ctypes
import time


class FilterFlipper:
    def __init__(self, deviceID):
        dll_name = 'Thorlabs.MotionControl.FilterFlipper.dll'
        self.__dll = ctypes.CDLL(dll_name)
        
        # c type definition
        self.WORD = ctypes.c_ushort
        self.WORD_P = ctypes.POINTER(self.WORD)
        self.DWORD = ctypes.c_ulong
        self.DWORD_P = ctypes.POINTER(self.DWORD)
        
        # function definition        
        
        self.TLI_BuildDeviceList = self.__dll.TLI_BuildDeviceList
        
        self.TLI_GetDeviceListSize = self.__dll.TLI_GetDeviceListSize
        
        self.TLI_GetDeviceListByTypeExt = self.__dll.TLI_GetDeviceListByTypeExt
        
        self.FF_Open = self.__dll.FF_Open
        self.FF_Open.argtypes = [ctypes.c_char_p]
        
        self.FF_Close = self.__dll.FF_Close
        self.FF_Close.argtypes = [ctypes.c_char_p]

        self.FF_CheckConnection = self.__dll.FF_CheckConnection
        self.FF_CheckConnection.argtypes = [ctypes.c_char_p]
        self.FF_CheckConnection.restype = ctypes.c_bool

        self.FF_GetNumberPositions = self.__dll.FF_GetNumberPositions
        self.FF_GetNumberPositions.argtypes = [ctypes.c_char_p]
        self.FF_GetNumberPositions.restype = ctypes.c_int

        self.FF_GetPosition = self.__dll.FF_GetPosition
        self.FF_GetPosition.argtypes = [ctypes.c_char_p]
        self.FF_GetPosition.restype = ctypes.c_short

        self.FF_Home = self.__dll.FF_Home
        self.FF_Home.argtypes = [ctypes.c_char_p]

        self.FF_MoveToPosition = self.__dll.FF_MoveToPosition
        self.FF_MoveToPosition.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.FF_MoveToPosition.restype = ctypes.c_short

        self.FF_RequestStatus = self.__dll.FF_RequestStatus
        self.FF_RequestStatus.argtypes = [ctypes.c_char_p]
        self.FF_RequestStatus.restype = ctypes.c_short
        
        # self.SBC_StartPolling = self.__dll.SBC_StartPolling
        # self.SBC_StartPolling.argtypes = [ctypes.c_char_p,ctypes.c_short,ctypes.c_int]
        # self.SBC_StartPolling.restype = ctypes.c_bool
        #
        # self.SBC_StopPolling = self.__dll.SBC_StopPolling
        # self.SBC_StopPolling.argtypes = [ctypes.c_char_p,ctypes.c_short]
        #
        # self.SBC_ClearMessageQueue = self.__dll.SBC_ClearMessageQueue
        # self.SBC_ClearMessageQueue.argtypes = [ctypes.c_char_p,ctypes.c_short]
        #
        # self.SBC_WaitForMessage = self.__dll.SBC_WaitForMessage
        # SBC_WaitForMessage.argtypes = [ctypes.c_char_p,ctypes.c_short,self.WORD_P,self.WORD_P,self.DWORD_P]
        # SBC_WaitForMessage.restype = ctypes.c_bool
        #
        # self.SBC_GetStatusBits = self.__dll.SBC_GetStatusBits
        # self.SBC_GetStatusBits.argtypes = [ctypes.c_char_p,ctypes.c_short]
        # self.SBC_GetStatusBits.restype = self.DWORD
        #
        #
        # variables definition
        self.deviceID = deviceID
        self.serialnum = None
        self.messageType = self.WORD(0)
        self.messageId = self.WORD(0)
        self.messageData = self.DWORD(0)

        self.isOpen = False

    def Initialize(self):
        # initialize
        self.TLI_BuildDeviceList()
        if self.TLI_GetDeviceListSize() == 0:
            print("No device detected. Please check.")
            return False

        buffersize = 100
        ReadBuffer = ctypes.create_string_buffer(b'\000'*buffersize)
        returncode = self.TLI_GetDeviceListByTypeExt(ReadBuffer, buffersize, self.deviceID)
        if returncode!=0:
            print(returncode)
            return False
        self.serialnum = ReadBuffer.value.decode('ascii').strip(',').encode('ascii')
        print(self.serialnum)
        return True
        
    def Open(self):
        if self.isOpen:
            return
        if self.serialnum is None:
            print("Please Initialise First")
            return False
        returncode = self.FF_Open(self.serialnum)
        if returncode != 0:
            print(returncode)
            return False
        self.isOpen = True
        return True

    def Close(self):
        if self.isOpen is False:
            return
        self.FF_Close(self.serialnum)
        self.isOpen = False
        return True

    def CheckConnection(self):
        return self.FF_CheckConnection(self.serialnum)

    def GetNumberPositions(self):
        return self.FF_GetNumberPositions(self.serialnum)

    def GetPosition(self):
        self.FF_RequestStatus(self.serialnum)
        time.sleep(0.1)
        temp_position = self.FF_GetPosition(self.serialnum)
        if temp_position == 3:
            return 1
        elif temp_position == 0:
            return 2
        else:
            print(temp_position)
            return None

    def Home(self, blocking=False):
        returncode = self.FF_Home(self.serialnum)
        if returncode != 0:
            print(returncode)
            return False
        if blocking:
            while self.GetPosition() != 1:
                time.sleep(0.5)
        return True

    def MoveToPosition(self, position, blocking=False):
        returncode = self.FF_MoveToPosition(self.serialnum, position)
        if returncode != 0:
            print(returncode)
            return False
        if blocking:
            while self.GetPosition() != position:
                time.sleep(0.5)
        return True

    def isConnected(self):
        return self.CheckConnection()


if __name__ == "__main__":
    SN = 37860818  # starting with 2 digits representing the device type and a 6 digit unique value.
    
    deviceID = 37
    FF = FilterFlipper(deviceID)
    FF.Initialize()
    FF.Open()
    if FF.isConnected:
        print(FF.GetPosition())
        FF.Home(True)
        print("Homed, Position:{}".format(FF.GetPosition()))
        print("Move to Position 1")
        FF.MoveToPosition(1, True)
        print("Now: {}".format(FF.GetPosition()))
        print("Move to Position 2")
        FF.MoveToPosition(2, True)
        print("Now: {}".format(FF.GetPosition()))
        FF.Home()
        print("Homed, Position:{}".format(FF.GetPosition()))
        FF.Close()
        print("Exit Elegantly")
