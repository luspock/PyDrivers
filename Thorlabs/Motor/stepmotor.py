import ctypes
import time


class StepMotor:
    def __init__(self, deviceID):
        dll_name = 'Thorlabs.MotionControl.Benchtop.StepperMotor.dll'
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
        
        self.SBC_Open = self.__dll.SBC_Open
        self.SBC_Open.argtypes = [ctypes.c_char_p]
        
        self.SBC_Close = self.__dll.SBC_Close
        self.SBC_Close.argtypes = [ctypes.c_char_p]
        
        self.SBC_EnableChannel = self.__dll.SBC_EnableChannel
        self.SBC_EnableChannel.argtypes = [ctypes.c_char_p, ctypes.c_short]
        
        self.SBC_DisableChannel = self.__dll.SBC_DisableChannel
        self.SBC_DisableChannel.argtypes = [ctypes.c_char_p, ctypes.c_short]
        
        self.SBC_StartPolling = self.__dll.SBC_StartPolling
        self.SBC_StartPolling.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_int]
        self.SBC_StartPolling.restype = ctypes.c_bool
        
        self.SBC_StopPolling = self.__dll.SBC_StopPolling
        self.SBC_StopPolling.argtypes = [ctypes.c_char_p, ctypes.c_short]
        
        self.SBC_ClearMessageQueue = self.__dll.SBC_ClearMessageQueue
        self.SBC_ClearMessageQueue.argtypes = [ctypes.c_char_p, ctypes.c_short]
        
        self.SBC_WaitForMessage = self.__dll.SBC_WaitForMessage
        SBC_WaitForMessage.argtypes = [ctypes.c_char_p, ctypes.c_short, self.WORD_P, self.WORD_P, self.DWORD_P]
        SBC_WaitForMessage.restype = ctypes.c_bool

        self.SBC_GetStatusBits = self.__dll.SBC_GetStatusBits
        self.SBC_GetStatusBits.argtypes = [ctypes.c_char_p, ctypes.c_short]
        self.SBC_GetStatusBits.restype = self.DWORD
        
        self.SBC_Home = self.__dll.SBC_Home
        self.SBC_Home.argtypes = [ctypes.c_char_p, ctypes.c_short]
        
        self.SBC_GetPosition = self.__dll.SBC_GetPosition
        self.SBC_GetPosition.argtypes = [ctypes.c_char_p, ctypes.c_short]
        self.SBC_GetPosition.restype = ctypes.c_int
        
        self.SBC_MoveToPosition = self.__dll.SBC_MoveToPosition
        self.SBC_MoveToPosition.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_int]
        self.SBC_MoveToPosition.restype = ctypes.c_short
        
        self.SBC_GetVelParams = self.__dll.SBC_GetVelParams
        self.SBC_GetVelParams.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        
        self.SBC_SetVelParams = self.__dll.SBC_SetVelParams
        self.SBC_SetVelParams.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_int, ctypes.c_int]
        
        self.SBC_GetRealValueFromDeviceUnit = self.__dll.SBC_GetRealValueFromDeviceUnit
        self.SBC_GetRealValueFromDeviceUnit.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.c_int]

        self.SBC_GetDeviceUnitFromRealValue = self.__dll.SBC_GetDeviceUnitFromRealValue
        self.SBC_GetDeviceUnitFromRealValue.argtypes = [ctypes.c_char_p, ctypes.c_short, ctypes.c_double, ctypes.POINTER(ctypes.c_int), ctypes.c_int]

        self.SBC_GetStageAxisMinPos = self.__dll.SBC_GetStageAxisMinPos
        self.SBC_GetStageAxisMinPos.argtypes = [ctypes.c_char_p, ctypes.c_short]
        self.SBC_GetStageAxisMinPos.restype = ctypes.c_int

        self.SBC_GetStageAxisMaxPos = self.__dll.SBC_GetStageAxisMaxPos
        self.SBC_GetStageAxisMaxPos.argtypes = [ctypes.c_char_p, ctypes.c_short]
        self.SBC_GetStageAxisMaxPos.restype = ctypes.c_int

        self.SBC_CheckConnection = self.__dll.SBC_CheckConnection
        self.SBC_CheckConnection.argtypes = [ctypes.c_char_p]

        # variables definition
        self.deviceID = deviceID
        self.serialnum = None
        self.messageType = self.WORD(0)
        self.messageId = self.WORD(0)
        self.messageData = self.DWORD(0)

        self.isOpen = False

    def initialize(self):
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
        return True
        
    def open(self):
        if self.isOpen:
            return
        if self.serialnum is not None:
            print("Please Initialise First")
            return False
        returncode = self.SBC_Open(self.serialnum)
        if returncode != 0:
            print(returncode)
            return False
        self.isOpen = True
        return True

    def close(self):
        if self.isOpen is False:
            return
        returncode = self.SBC_Close(self.serialnum)
        if returncode != 0:
            print(returncode)
            return False
        self.isOpen = False
        return True
        
    
if __name__ == "__main__":
    deviceID = 40
    SM = StepMeter(deviceID)
    SM.initialise()
    SM.open()
    print("StartPolling: {}".format(SM.SBC_StartPolling(SM.serialnum,1,200)))
    SM.close()
    


time.sleep(3)
print("EnableChannel: {}".format(SBC_EnableChannel(serialnum,1)))

print("ClearMessageQueue: {}".format(SBC_ClearMessageQueue(serialnum,1)))

time.sleep(0.5)
SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))
print("Move Home Position: {}".format(SBC_Home(serialnum,1)))
print("Device {} is homing".format(serialnum.decode('ascii')))
SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))

status_bits = SBC_GetStatusBits(serialnum,1)
print(hex(status_bits),type(status_bits))
time.sleep(0.2)
position = SBC_GetPosition(serialnum,1)
realunit = ctypes.c_double(0)
print("Position: {}".format(position))
print("Real Unit: {}".format(SBC_GetRealValueFromDeviceUnit(serialnum,1,position,ctypes.byref(realunit),0)))

acceleration = ctypes.c_int(0)
maxVelocity = ctypes.c_int(0)
print(SBC_GetVelParams(serialnum,1,ctypes.byref(acceleration),ctypes.byref(maxVelocity)))
print("Acceleration: {}".format(acceleration.value),"maxVelocity: {}".format(maxVelocity.value))
print(SBC_SetVelParams(serialnum,1,acceleration,maxVelocity))

time.sleep(1)
SBC_ClearMessageQueue(serialnum,1)
SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))
print(SBC_MoveToPosition(serialnum,1,2000))
SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))

time.sleep(10)
SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))

print("DisableChannel: {}".format(SBC_DisableChannel(serialnum,1)))
SBC_StopPolling(serialnum,1)
print("StopPolling")

print("Close: {}".format(SBC_Close(serialnum)))

#TLI_GetDeviceList
#TLI_GetDeviceListByType
#TLI_GetDeviceListByTypes
#TLI_GetDeviceInfo

