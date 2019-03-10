import ctypes


class Superchrome:
    def __init__(self):
        self.__dll = ctypes.WinDLL("SuperChromeSDK.dll")

        # Prototype
        # self.__ConfigureModule = __dll.ConfigureModule
        # self.__ConfigureModule.restype = ctypes.c_int
        #
        # self.__EditCalibration = __dll.EditCalibration
        # self.__EditCalibration.restype = ctypes.c_int
        #
        # self.__GetCurrentBw = __dll.GetCurrentBw
        # self.__GetCurrentBw.argtypes = [c_double*1]
        # self.__GetCurrentBw.restype = ctypes.c_int

    def ConfigureModule(self):
        """
        Description:The purpose of this function is to configure
                    the motor drives of the SuperChrome module.
                    It is separate from the TSelector object
                    as the configuration can be changed
                    irrespective of whether there is hardware present.
        Parameters: None
        """
        return self.__dll.ConfigureModule()

    def EditCalibration(self):
        """
        Description: This function is used to edit the current calibration values.
        Parameters: None
        """
        return self.__dll.EditCalibration()

    def GetCurrentBw(self):
        """
        Description: This function is used to return the current bandwidth for a dual filter.
        Parameters: BW will contain the filter bandwidth.
        """
        BW = ctypes.c_double()
        returncode = self.GetCurrentBw(ctypes.byref(BW))
        return returncode,BW.value

    def GetCurrentDistance(self,FilterNum):
        """
        Description: This function is used to return the current distance
                    from the home position (in mm) for the specified filter.
        Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    Dist will contain the distance value.
        """
        Dist = ctypes.c_double()
        returncode = self.__dll.GetCurrentDistance(ctypes.c_int(FilterNum),ctypes.byref(Dist))
        return returncode, Dist.value

    def GetCurrentSteps(self, FilterNum):
        """
        Description: This function is used to return the current distance
                    from the home position (in motor steps) for the specified filter.
        Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    Steps will contain the position in steps.
        """
        Steps = ctypes.c_int
        returncode = self.__dll.GetCurrentSteps(ctypes,c_int(FilterNum),ctypes.byref(Steps))
        return returncode, Steps.value

    def GetCurrentWave(self, FilterNum):
        """
        Description: This function is used to return the current wavelength of the specified filter.
        Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    Wave will contain the position in nanometres according to the current calibration values.
        """
        Wave = ctypes.c_double()
        returncode = self.__dll.GetCurrentWave(ctypes.c_int(FilterNum),ctypes.byref(Wave))
        return returncode, Wave.value

    def GetCurrentWaveDual(self):
        """
        Description: This function is used to return the current wavelength
                    for a dual filter.
        Parameters: DualWave will contain the combined wavelength in nanometres
                    according to the current calibration values.
        """
        DualWave = ctypes.c_double()
        returncode = self.__dll.GetCurrentWaveDual(ctypes.byref(DualWave))
        return returncode, DualWave.value

    def GetSerialNum(self):
        """
        Description: This function is used to return the serial number of a filter module.
        Parameters: SerNum will contain the serial number of the module.
                    This will normally be less than 20 characters long,
                    so the calling programme will have to allocate sufficient memory
                    for the parameter in advance of calling the function.
        """
        SerNum = ctypes.create_string_buffer(b'\000'*100)
        returncode = self.__dll.GetSerialNum(SerNum)
        return returncode, SerNum.value.decode("ascii")

    def GetDualWaveMax(self):
        """
        Description: This function is used to return the common wavelength maximum
                    for a dual filter.
        Parameters: WaveMax will contain the maximum wavelength obtainable
                    when both filters are being used in combination.
        """
        WaveMax = ctypes.c_double()
        returncode = self.__dll.GetDualWaveMax(ctypes.byref(WaveMax))
        return returncode, WaveMax.value

    def GetDualWaveMin(self):
        """
        Description: This function is used to return the common wavelength minimum
                    for a dual filter.
        Parameters: WaveMin will contain the minimum wavelength obtainable
                    when both filters are being used in combination.
        """
        WaveMin = ctypes.c_double()
        returncode = self.__dll.GetDualWaveMin(ctypes.byref(WaveMin))
        return returncode, WaveMin.value

    def GetFilterActive(self, FilterNum):
        """
        Description: This function is used to return whether the specified filter is active
                    (i.e. is in the beam path. Zero is inactive; otherwise active.
        Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    Active will contain the active status of the filter.
        """
        Active = ctypes.c_int()
        returncode = self.__dll.GetFilterActive(ctypes.c_int(FilterNum), ctypes.byref(Active))
        return returncode, Active.value

    def GetFilterCalibrated(self, FilterNum):
        """
        Description: This function is used to return whether the specified filter has been calibrated.
                    Zero is uncalibrated; otherwise calibrated.
        Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    Cal will contain the calibration status of the filter.
        """
        Cal = ctypes.c_int()
        returncode = self.__dll.GetFilterCalibrated(ctypes.c_int(FilterNum), ctypes.byref(Cal))
        return returncode, Cal.value

    def GetFilterDual(self):
        """
        Description: This function is used to return whether the specified filter is a dual filter
                    (i.e. has two separate filters driven by different motors. Zero is false; otherwise true.
        Parameters: IsDual will contain the dual filter status of the filter.
        """
        IsDual = ctypes.c_int()
        returncode = self.__dll.GetFilterDual(ctypes.byref(IsDual))
        return returncode, IsDual.value

    def GetWaveMax(self, FilterNum):
        """
        Description: This function is used to return the wavelength maximum for the specified filter.
                    Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    WaveMax will contain the maximum wavelength for the filter as set in the configuration procedure.
        """
        WaveMax = ctypes.c_double()
        returncode = self.__dll.GetWaveMax(ctypes.c_int(FilterNum), ctypes.byref(WaveMax))
        return returncode, WaveMax.value

    def GetWaveMin(self, FilterNum):
        """
        Description: This function is used to return the wavelength minimum for the specified filter.
        Parameters: FilterNum is the number of the filter (1 or 2) being queried.
                    WaveMin will contain the minimum wavelength for the filter as set in the configuration procedure.
        """
        WaveMin = ctypes.c_double()
        returncode = self.__dll.GetWaveMin(ctypes.c_int(FilterNum), ctypes.byref(WaveMin))
        return returncode, WaveMin.value

    def InitialiseDll(self, AppHandle):
        """
        Description: This function is used to pass the application handle to the DLL.
        Parameters: AppHandle is the windows of the external programme or window calling rge DLL.
        """
        #something uncompleted
        return self.__dll.InitialiseDll(AppHandle)

    def Initialise(self):
        """
        Description: This function attempts to initialise the filter device by first
                    creating the appropriate filter object and then trying to initialise it.
        Parameters: None.
        """
        return self.__dll.Initialise()

    def MoveDistance(self, FilterNum, Dist):
        """
        Description: This function is used to move the specified filter to the passed position in mm.
        Parameters: FilterNum is the number of the filter (1 or 2) to be moved.
                    Dist is the position that the filter is to be moved to.
        """
        return self.__dll.MoveDistance(ctypes.c_int(FilterNum), ctypes.c_double(Dist))

    def MoveOutOfPath(self, FilterNum):
        """
        Description: This function is used to move the specified filter out of the beam path.
        Parameters: FilterNum is the number of the filter (1 or 2) to be moved.
        """
        return self.__dll.MoveOutOfPath(ctypes.c_int(FilterNum))

    def MoveSteps(self, FilterNum, Steps):
        """
        Description: This function is used to move the specified filter to the passed position in steps.
        Parameters: FilterNum is the number of the filter (1 or 2) to be moved.
                    Steps is the position that the filter is to be moved to.
        """
        return self.__dll.MoveSteps(ctypes.c_int(FilterNum), ctypes.c_int(Steps))

    def MoveSyncWave(self, Lambda1, Lambda2):
        """
        Description: This function is used to perform a synchronous wavelength move for a dual filter.
        Parameters: Lambda1 is the wavelength for filter 1.
                    Lambda2 is the wavelength for filter 2.
        """
        return self.__dll.MoveSyncWave(ctypes.c_double(Lambda1), ctypes.c_double(Lambda2))

    def MoveSyncWaveAndBw(self, Lambda, Bw):
        """
        Description: This function is used to move a dual filter to a specified wavelength and bandwidth combination.
        Parameters: Lambda is the wavelength for the filter combination.
                    BW is the bandwidth for the filter combination.
        """
        return self.__dll.MoveSyncWaveAndBw(ctypes.c_double(Lambda), ctypes.c_double(Bw))

    def MoveWavelength(self, FilterNum, Lambda):
        """
        Description: This function is used to move the specified filter to the passed position in nm.
        Parameters: FilterNum is the number of the filter (1 or 2) to be moved.
                    Lambda is the wavelength that the filter is to be moved to.
        """
        return self.__dll.MoveWavelength(ctypes.c_int(FilterNum), ctypes.c_double(Lambda))

    def ReleaseDll(self):
        """
        Description: This procedure is used to free the local objects prior to the DLL being closed.
        Parameters: None.
        """
        return self.__dll.ReleaseDll()

    def RunCalibration(self):
        """
        Description: This function is used to run a calibration process.
        Parameters: None
        """
        return self.__dll.RunCalibration()


if __name__ == "__main__":
    mysuperchrome = Superchrome()
    # handle = ctypes.windll.kernel32.GetModuleHandleW(None)
    handle = ctypes.windll.kernel32.GetConsoleWindow()
    # print(type(handle))
    # print(handle)
    print("Initialise Dll: " + str(mysuperchrome.InitialiseDll(handle)))
    
    print("Initialise Start")
    print(mysuperchrome.Initialise())
    print("Initialise End")

    # print(mysuperchrome.ConfigureModule())
    # print(mysuperchrome.EditCalibration())

    [returncode, cal] = mysuperchrome.GetFilterCalibrated(1)
    print(returncode)
    print(cal)

    # print(mysuperchrome.RunCalibration())
    print(mysuperchrome.MoveSyncWaveAndBw(600.0, 25.0))
    print(mysuperchrome.GetSerialNum())
    print("ReleaseDll: " + str(mysuperchrome.ReleaseDll()))
