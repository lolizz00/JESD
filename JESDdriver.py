import cp2130
from cp2130.data import *
import struct
import time

class JESD:

    BYTEORDER = 'big'

    def __del__(self):
        try:
            self.disconnect()
        except:
            pass

    def clearStatus(self):
        self.write(0x182, 1)
        self.write(0x182, 0)

        self.write(0x183, 1)
        self.write(0x183, 0)

    def checkStatus(self, n):

        reg = None
        if n == 1:
            reg = self.read(0x182)
        elif n == 2:
            reg = self.read(0x183)


        lostMsk = (1 << 2)
        ldMask = (1 << 1)

        res = ""

        if not (reg & ldMask):
            res = "PLL LOW"

        if reg & lostMsk:
            res = res + " Edge Fails"

        if res == "":
            return "OK"
        else:
            return res


    def isConnected(self):
        if self.handle:
            return True
        else:
            return False

    def __init__(self):
        self.slave = None
        self.cs = None
        self.chip = None
        self.handle = None


    def invertPin(self, val):
        if val == LogicLevel.HIGH:
           return LogicLevel.LOW
        else:
            return LogicLevel.HIGH

    def LEDBlink(self):
        gpio1 = self.chip.gpio1

        for i in range(4):
            gpio1.value = self.invertPin(gpio1.value)
            time.sleep(0.5)
            gpio1.value = self.invertPin(gpio1.value)
            time.sleep(1)

    def getListStr(self):
        lst = cp2130.list()

        for i in range(len(lst)):
            lst[i] = str(lst[i])

        return lst

    def set4Wire(self):
        self.write(0x0, 0x10)  # 3 wire disabled, 4 бит
        self.write(0x14A, 0x33)  # reset pin , output[0:2], SPI Readback[3:5]

    def reset(self):
        self.write(0x0, 0x80) # сброс, 7 бит

    def enableWrite(self):
        self.write(0x1FFD, 0x0)
        self.write(0x1FFE, 0x0)
        self.write(0x1FFF, 0x53)

    def connect(self, id):

        tmp  = cp2130.connectID(id)
        self.chip = tmp[0]
        self.handle = tmp[1]

        self.slave = self.chip.channel1
        self.slave.cs_toggle = False
        self.slave.spi_mode = SPIMode.of(ClockPolarity.IDLE_LOW, ClockPhase.LEADING_EDGE)
        self.slave.clock_frequency = 750000

        self.signal = self.chip.gpio0
        self.signal.mode = OutputMode.PUSH_PULL
        self.signal.value = LogicLevel.HIGH

        self.set4Wire()

        prod = (self.read(0x4) << 7) |  self.read(0x5)

        return  hex(prod)

    # вроде ок
    def write(self, addr, val):

        addr = (addr & (~0x8000))  & 0xFFFF

        b_addr = addr.to_bytes(2, byteorder=self.BYTEORDER)
        b_val =  val.to_bytes(1, byteorder=self.BYTEORDER)

        bytes = b_addr + b_val

        self.signal.value = LogicLevel.LOW
        self.slave.write(bytes)
        self.signal.value = LogicLevel.HIGH


    def read(self, addr):
        addr = (addr | 0x8000 & 0xFFFF)
        b_addr = addr.to_bytes(2, byteorder=self.BYTEORDER)
        self.signal.value = LogicLevel.LOW
        self.slave.write(b_addr)
        val = self.slave.read(1)
        self.signal.value = LogicLevel.HIGH
        val = int(val[0])
        return val

    def disconnect(self):

        if not self.handle:
            return

        try:
            self.handle.close()
        except:
            pass


        self.handle = None


        self.slave = None
        self.signal = None
        self.chip = None