import clr

# pythonnet is required
clr.AddReference("Thorlabs.PM100D_32.Interop")

from Thorlabs.PM100D_32.Interop import PM100D
from System import Double


class PM_Thorlabs():
    def __init__(self):
        self.identifier = "USB0::0x1313::0x8078::P0011895::INSTR"
        self.instance = None
        self.temp_double = Double(0)
        self.MaxWavelength = 1100
        self.MinWavelength = 400

    def connect(self):
        self.instance = PM100D(self.identifier,True,True)

    def setWavelength(self, wavelength):
        if self.MinWavelength < wavelength < self.MaxWavelength:
            return True if self.instance.setWavelength(wavelength) == 0 else False
        else:
            return False

    def getWavelength(self):
        ret = self.instance.getWavelength(0, self.temp_double)
        if ret[0] == 0:
            return ret[1]
        else:
            return None

    def getPower(self):
        ret = self.instance.measPower(self.temp_double)
        if ret[0] == 0:
            return ret[1]
        else:
            return None

    def close(self):
        self.instance.Dispose()    


if __name__ == "__main__":
    pm = PM_Thorlabs()
