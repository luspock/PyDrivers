import ctypes
import time

class BPC():
    """Load dll and define functions"""
    def __init__(self,deviceID):
        dll_name = 'Thorlabs.MotionControl.Benchtop.Piezo.dll'
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
        
        self.PBC_Open = self.__dll.PBC_Open
        self.PBC_Open.argtypes = [ctypes.c_char_p]
        
        self.PBC_Close = self.__dll.PBC_Close
        self.PBC_Close.argtypes = [ctypes.c_char_p]

        self.PBC_CheckConnection = self.__dll.PBC_CheckConnection
        self.PBC_CheckConnection.argtypes = [ctypes.c_char_p]
        self.PBC_CheckConnection.restype = ctypes.c_bool

        self.PBC_MaxChannelCount = self.__dll.PBC_MaxChannelCount
        self.PBC_MaxChannelCount.argtypes = [ctypes.c_char_p]
        self.PBC_MaxChannelCount.restype = ctypes.c_int

        #self.PBC_SetPositionControlMode = self.__dll.PBC_SetPositionControlMode

        self.PBC_SetPosition = self.__dll.PBC_SetPosition
        self.PBC_SetPosition.argtypes = [ctypes.c_char_p,ctypes.c_short,ctypes.c_short]
        self.PBC_SetPosition.restype = ctypes.c_short

        self.PBC_GetPosition = self.__dll.PBC_GetPosition
        self.PBC_GetPosition.argtypes = [ctypes.c_char_p,ctypes.c_short]
        self.PBC_GetPosition.restype = ctypes.c_short

        self.PBC_IsChannelValid = self.__dll.PBC_IsChannelValid
        self.PBC_IsChannelValid.argtypes = [ctypes.c_char_p,ctypes.c_short]
        self.PBC_IsChannelValid.restype = ctypes.c_bool

        self.PBC_GetNumChannels = self.__dll.PBC_GetNumChannels
        self.PBC_GetNumChannels.argtypes = [ctypes.c_char_p]
        self.PBC_GetNumChannels.restype = ctypes.c_short

        """
            Gets the maximum travel of the device. 
            This requires an actuator with built in position sensing
            Parameters:
                serialNo The controller serial no.  
                channel The channel (1 to n).  
            Returns:
                The distance in steps of 100nm,
            range 0 to 65535 (10000 is equivalent to 1mm). 
        """
        self.PBC_GetMaximumTravel = self.__dll.PBC_GetMaximumTravel
        self.PBC_GetMaximumTravel.argtypes = [ctypes.c_char_p,ctypes.c_short]
        self.PBC_GetMaximumTravel.restype = ctypes.c_ushort # WORD

        self.PBC_StartPolling = self.__dll.PBC_StartPolling
        self.PBC_StartPolling.argtypes = [ctypes.c_char_p,ctypes.c_short,ctypes.c_int]
        self.PBC_StartPolling.restype = ctypes.c_bool
        
        self.PBC_StopPolling = self.__dll.PBC_StopPolling
        self.PBC_StopPolling.argtypes = [ctypes.c_char_p,ctypes.c_short]
        self.PBC_StopPolling.restype = ctypes.c_bool

        self.PBC_LoadSettings = self.__dll.PBC_LoadSettings
        self.PBC_LoadSettings.argtypes = [ctypes.c_char_p, ctypes.c_short]
        self.PBC_LoadSettings.restype = ctypes.c_bool

        #self.SBC_ClearMessageQueue = self.__dll.SBC_ClearMessageQueue
        #self.SBC_ClearMessageQueue.argtypes = [ctypes.c_char_p,ctypes.c_short]
        
        #self.SBC_WaitForMessage = self.__dll.SBC_WaitForMessage
        #SBC_WaitForMessage.argtypes = [ctypes.c_char_p,ctypes.c_short,self.WORD_P,self.WORD_P,self.DWORD_P]
        #SBC_WaitForMessage.restype = ctypes.c_bool

        #self.SBC_GetStatusBits = self.__dll.SBC_GetStatusBits
        #self.SBC_GetStatusBits.argtypes = [ctypes.c_char_p,ctypes.c_short]
        #self.SBC_GetStatusBits.restype = self.DWORD
        

        # variables definition
        self.deviceID = deviceID
        self.serialnum = None
        self.messageType = self.WORD(0)
        self.messageId = self.WORD(0)
        self.messageData = self.DWORD(0)

        self.isOpen = False

    def Initialize(self):
        """initialize"""
        self.TLI_BuildDeviceList()
        if (self.TLI_GetDeviceListSize()==0):
            print("No device detected. Please check.")
            return False

        buffersize = 100
        ReadBuffer = ctypes.create_string_buffer(b'\000'*buffersize)
        returncode = self.TLI_GetDeviceListByTypeExt(ReadBuffer,buffersize,self.deviceID)
        if(returncode!=0):
            print(returncode)
            return False
        self.serialnum = ReadBuffer.value.decode('ascii').strip(',').encode('ascii')
        print(self.serialnum)
        return True
        
    def Open(self):
        if self.isOpen:
            return
        if(self.serialnum)== None:
            print("Please Initialise First")
            return False
        returncode = self.PBC_Open(self.serialnum)
        if(returncode != 0):
            print(returncode)
            return False
        self.isOpen = True
        return True

    def Close(self):
        if self.isOpen == False:
            return
        self.PBC_Close(self.serialnum)
        self.isOpen = False
        return True

    def CheckConnection(self):
        return self.PBC_CheckConnection(self.serialnum)

    def GetPosition(self,channel):
        """
        Gets the position when in closed loop mode. 
        The result is undefined if not in closed loop mode
        Parameters:
            serialNo The controller serial no.  
            channel The channel (1 to n).  
        Returns:
            The position as a percentage of maximum travel,
            range -32767 to 32767, equivalent to -100 to 100%.
        """
        return self.PBC_GetPosition(self.serialnum,channel)

    def MoveToPosition(self,channel,position,blocking=False):
        """ Position range 0-32767   0%-100%"""
        returncode = self.PBC_SetPosition(self.serialnum,channel,round(position/20*32767))
        time.sleep(0.5)
        if(returncode != 0):
            print(returncode)
            return False
        if blocking:
            delta = self.GetPosition(channel)-round(position/20*32767)
            #print(delta)
            while(delta>9):
                time.sleep(0.5)
                delta = self.GetPosition(channel)-round(position/20*32767)
                #print(delta)
        return True

    @property
    def isConnected(self):
        return self.CheckConnection();
    
if __name__ == "__main__":
 
    SN = 71856190 #starting with 2 digits representing the device type and a 6 digit unique value.
    
    deviceID = 71
    bpc = BPC(deviceID)
    bpc.Initialize()
    bpc.Open()
    print(bpc.isConnected)
    bpc.PBC_LoadSettings(bpc.serialnum,1)
    bpc.PBC_LoadSettings(bpc.serialnum,2)
    bpc.PBC_StartPolling(bpc.serialnum,1,200)
    bpc.PBC_StartPolling(bpc.serialnum,2,200)
    #print("Channel 1 Max Range: {} ".format(bpc.PBC_GetMaximumTravel(bpc.serialnum,1)))
    #print("Channel 2 Max Range: {} ".format(bpc.PBC_GetMaximumTravel(bpc.serialnum,2)))
    #print("Channel 3 Max Range: {} ".format(bpc.PBC_GetMaximumTravel(bpc.serialnum,3)))
    #print(bpc.PBC_MaxChannelCount(bpc.serialnum))
    #print("Channel1 Position: {}".format(bpc.GetPosition(1)))
    for x in range(3,13):
        bpc.MoveToPosition(1,x,True)
        for y in range(3,13):
            bpc.MoveToPosition(2,y,True)
            print("X:{0} Y:{1}".format(bpc.GetPosition(1),bpc.GetPosition(2)))
    # random move
    #for i in range(10):
    #    time.sleep(0.5)
    #    print(i)
    #    print(bpc.GetPosition(1))
    bpc.PBC_StopPolling(bpc.serialnum,1)
    bpc.PBC_StopPolling(bpc.serialnum,2)

    bpc.Close()
      

#
#time.sleep(3)
#print("EnableChannel: {}".format(SBC_EnableChannel(serialnum,1)))

#print("ClearMessageQueue: {}".format(SBC_ClearMessageQueue(serialnum,1)))

#time.sleep(0.5)
#SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
#print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))
#print("Move Home Position: {}".format(SBC_Home(serialnum,1)))
#print("Device {} is homing".format(serialnum.decode('ascii')))
#SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
#print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))

#status_bits = SBC_GetStatusBits(serialnum,1)
#print(hex(status_bits),type(status_bits))
#time.sleep(0.2)
#position = SBC_GetPosition(serialnum,1)
#realunit = ctypes.c_double(0)
#print("Position: {}".format(position))
#print("Real Unit: {}".format(SBC_GetRealValueFromDeviceUnit(serialnum,1,position,ctypes.byref(realunit),0)))

#acceleration = ctypes.c_int(0)
#maxVelocity = ctypes.c_int(0)
#print(SBC_GetVelParams(serialnum,1,ctypes.byref(acceleration),ctypes.byref(maxVelocity)))
#print("Acceleration: {}".format(acceleration.value),"maxVelocity: {}".format(maxVelocity.value))
#print(SBC_SetVelParams(serialnum,1,acceleration,maxVelocity))

#time.sleep(1)
#SBC_ClearMessageQueue(serialnum,1)
#SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
#print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))
#print(SBC_MoveToPosition(serialnum,1,2000))
#SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
#print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))

#time.sleep(10)
#SBC_WaitForMessage(serialnum,1,ctypes.pointer(messageType),ctypes.pointer(messageId),ctypes.pointer(messageData))
#print("messageType: {}".format(messageType.value),"messageId: {}".format(messageId.value),"messageData: {}".format(messageData.value))

#print("DisableChannel: {}".format(SBC_DisableChannel(serialnum,1)))
#SBC_StopPolling(serialnum,1)
#print("StopPolling")

#print("Close: {}".format(SBC_Close(serialnum)))

#TLI_GetDeviceList
#TLI_GetDeviceListByType
#TLI_GetDeviceListByTypes
#TLI_GetDeviceInfo
