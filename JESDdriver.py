import cp2130
from cp2130.data import *
import struct
import time

# класс для работы с JESD-иной

class JESD:


    # порядок байтов при отправке по SPI
    BYTEORDER = 'big'

    # дестркуттор
    def __del__(self):
        try:
            self.disconnect()
        except:
            pass


    # очистка статуса
    # RB_PLL1_LD_LOST, RB_PLL1_LD, CLR_PLL1_LD_LOST
    # RB_PLL2_LD_LOST, RB_PLL2_LD, CLR_PLL2_LD_LOST
    def clearStatus(self):
        self.write(0x182, 1)
        self.write(0x182, 0)

        self.write(0x183, 1)
        self.write(0x183, 0)


    # проверка статуса
    # RB_PLL1_LD_LOST, RB_PLL1_LD, CLR_PLL1_LD_LOST
    # RB_PLL2_LD_LOST, RB_PLL2_LD, CLR_PLL2_LD_LOST
    def checkStatus(self, n):

        reg = None

        # читаем соответствующий номер PLL регистр
        if n == 1:
            reg = self.read(0x182)
        elif n == 2:
            reg = self.read(0x183)


        lostMsk = (1 << 2) # LOST - 2 бит
        ldMask = (1 << 1) # LOW - 1 бит

        res = ""

        # проверяем бит
        if not (reg & ldMask):
            res = "PLL LOW"

        # проверяем бит и дописываем сообщение
        if reg & lostMsk:
            res = res + " Edge Fails"

        if res == "":
            return "OK"
        else:
            return res

    # проверка, живо ли устройство
    # если регистр читается(все равно как), ничего не отвалилось
    def isConnected(self):
        try:
            self.read(0x06)
            return True
        except:
            return False

    def __init__(self):
        self.slave = None
        self.cs = None
        self.chip = None
        self.handle = None

    # простое отрицание, на языке вот этой структуры
    def invertPin(self, val):
        if val == LogicLevel.HIGH:
           return LogicLevel.LOW
        else:
            return LogicLevel.HIGH

    # мигаем лампочкой
    def LEDBlink(self):
        gpio1 = self.chip.gpio1

        # несколько раз, так видно лучше
        for i in range(2):
            gpio1.value = self.invertPin(gpio1.value)
            time.sleep(0.5)
            gpio1.value = self.invertPin(gpio1.value)
            time.sleep(1)


    # получение списка доступных устройств
    def getListStr(self):
        lst = cp2130.list() # функция нестандартная, но как правил объяснять не буду (:

        for i in range(len(lst)):
            lst[i] = str(lst[i])

        return lst


    # переключение в режим с MOSI и MISO
    def set4Wire(self):
        self.write(0x0, 0x10)   # 3 wire disabled, 4 бит
        self.write(0x14A, 0x33)  # reset pin , output[0:2], SPI Readback[3:5]


    # сброс LMK
    def reset(self):
        self.write(0x0, 0x80) # сброс, 7 бит

    # разрешаем писать в регистры
    # SPI_LOCK
    def enableWrite(self):
        self.write(0x1FFD, 0x0)
        self.write(0x1FFE, 0x0)
        self.write(0x1FFF, 0x53)


    # подключение
    def connect(self, id):


        # подключаемся
        tmp  = cp2130.connectID(id)
        self.chip = tmp[0]
        self.handle = tmp[1]


        # настраиваем SPI канал
        self.slave = self.chip.channel1
        self.slave.cs_toggle = False
        self.slave.spi_mode = SPIMode.of(ClockPolarity.IDLE_LOW, ClockPhase.LEADING_EDGE)
        self.slave.clock_frequency = 750000

        # СS будем дергать вручную
        self.signal = self.chip.gpio0
        self.signal.mode = OutputMode.PUSH_PULL
        self.signal.value = LogicLevel.HIGH

        self.set4Wire()

        # возвращаем номер, просто что бы проверить, что данные читаются
        prod = (self.read(0x4) << 7) |  self.read(0x5)

        return  hex(prod)

    # запись в регистр
    def write(self, addr, val):

        addr = (addr & (~0x8000))  & 0xFFFF # сбрасываем бит чтения

        b_addr = addr.to_bytes(2, byteorder=self.BYTEORDER) # переводим адрес и значение в байты
        b_val =  val.to_bytes(1, byteorder=self.BYTEORDER)

        bytes = b_addr + b_val # собираем байты в одну кучку1

        self.signal.value = LogicLevel.LOW # дергаем CS
        self.slave.write(bytes) # записываем
        self.signal.value = LogicLevel.HIGH


    def read(self, addr):
        addr = (addr | 0x8000 & 0xFFFF) # ставим бит чтения
        b_addr = addr.to_bytes(2, byteorder=self.BYTEORDER) # переводим адрес в байты
        self.signal.value = LogicLevel.LOW # дергаем CS
        self.slave.write(b_addr) # пишем
        val = self.slave.read(1) # читаем
        self.signal.value = LogicLevel.HIGH # отпускаем CS
        val = int(val[0]) # переводим в int
        return val


    # отключение
    def disconnect(self):

        if not self.handle:
            return

        try:
            self.handle.close() # закрываем handler libusb
        except:
            pass

        # и к чертям все закрываем, деструкторы сами разберутся
        self.handle = None
        self.slave = None
        self.signal = None
        self.chip = None