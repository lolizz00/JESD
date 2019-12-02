from PyQt5 import QtCore, QtGui, QtWidgets
from mw import Ui_MainWindow
from version import version_logo
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon
from datetime import datetime
from JESDdriver import JESD
from selectForm import SW



class MW(QtWidgets.QMainWindow, Ui_MainWindow):


    # заново открыть окно выбора устройства
    def recPushButtonClicked(self):
        self.dev.disconnect()
        self.hide()
        self.sw.show()


    # сюда ловим сигнал из окошка о выбранном устройстве
    def selectSlot(self, ind):
        info = None
        try:
            info = self.dev.connect(ind)
            self.checkStatus()
        except Exception as e:
            self.showErr('Ошибка при подключении: ' + str(e))
            self.writeLog('Ошибка при подключении: ' + str(e))

            return

        self.writeLog('Подключено к устройству #' + str(ind) + ' ' + str(self.dev.getListStr()[ind]))

        self.show()

    # сброс LMK
    def resetPushButtonClicked(self):
        self.dev.reset()
        self.dev.set4Wire()
        self.dev.enableWrite()


        self.writeLog('Устройство сброшено.')

    # считать последний открытый файл
    def getLastFile(self):

        try:
            f = open('lf', 'r')
            line = f.readline()
            f.close()
            return line
        except: # если его нет, игнорируем
            return ""


    # сохраняем путь к файлу, который открыли
    def saveLastFile(self, path):
        f = open('lf', 'w')
        f.write(path)
        f.close()

    # очистка статуса устройства
    def clearStatus(self):
        self.dev.clearStatus()
        self.writeLog('Статус устройства очищен.')
        self.checkStatus()

    # тихая проверка статуса устройсва(без записей в лог)
    def checkStatusQuite(self):
        stat1 = self.dev.checkStatus(1)
        stat2 = self.dev.checkStatus(2)

        self.pll1Label.setText(stat1)
        self.pll2Label.setText(stat2)

        if stat1 != "OK":
            self.tTimer.stop()
            self.autoStatCheckBox.setChecked(False)
            self.writeLog('Обнаружена ошибка, автообновление статуса остановлено')

            self.pll1Label.setStyleSheet("color: red") # цвет надписи
        else:
            self.pll1Label.setStyleSheet("color: black")

        if stat2 != "OK":
            self.tTimer.stop()
            self.autoStatCheckBox.setChecked(False)
            self.writeLog('Обнаружена ошибка, автообновление статуса остановлено')

            self.pll2Label.setStyleSheet("color: red")
        else:
            self.pll2Label.setStyleSheet("color: black")

    # проверка статуса в записью в лог
    def checkStatus(self):

        self.writeLog('Проверяем статус PLL...')
        stat1 = self.dev.checkStatus(1)

        self.writeLog('PLL1 status: ' + stat1)

        self.pll1Label.setText(stat1)
        if stat1 != "OK":
            self.pll1Label.setStyleSheet("color: red")
        else:
            self.pll1Label.setStyleSheet("color: black")

        stat2 = self.dev.checkStatus(2)
        self.writeLog('PLL2 status: ' + stat2)

        self.pll2Label.setText(stat2)
        if stat2 != "OK":
            self.pll2Label.setStyleSheet("color: red")
        else:
            self.pll2Label.setStyleSheet("color: black")

    # автообновление статуса
    def autoStatCheckBoxHandle(self):
        if self.autoStatCheckBox.isChecked():
            self.stTimer.start(5000) # отмечено - пускаем таймер
        else:
            self.stTimer.stop()  # снято - отсанавливаем таймер

    def __init__(self):
        super(MW, self).__init__()
        self.setupUi(self)

        self.setWindowTitle('JESD_8SYNCV01 ver: ' + version_logo) # отображаем версию ПО


        self.setCentralWidget(self.cw)
        self.initSlots()
        self.dev = JESD()

        # последний считанный файл
        self.fileLineEdit.setText(self.getLastFile())

        # для удобства
        self.toolBox.setCurrentIndex(0)


        # проверка, что устройство не отвалилось
        self.timer = QtCore.QTimer()
        self.timer.start(5000)
        self.timer.timeout.connect(self.checkDev)


        # таймер для проверки статуса
        self.stTimer = QtCore.QTimer()
        self.stTimer.timeout.connect(self.checkStatusQuite)

        # окно выбора устройства
        self.sw = SW()
        self.sw.selectSignal.connect(self.selectSlot) # ловим сигнал о выборе

        self.sw.show()


    # проверка, что устройство не отвалилось в таймере
    def checkDev(self):
        if not self.dev.isConnected()  and not self.isHidden(): # не делаем, если устройство скрыто
            try:
                self.dev.read(0x0)
            except:
                txt = 'Устройство было неожиданно отключено'
                self.writeLog(txt) # отчитываемся
                self.showErr(txt)
                self.recPushButtonClicked() # снова открываем окно

    # парсинг файла
    def parseFile(self, fname):


        regs = []
        vals = []


        # перетыкаемся в нужный режим
        self.dev.set4Wire()

        try:

            # открыли файл
            fd = open(fname, 'r')
            flg = True

            self.writeLog('Запись файла \'' + fname + '\' ...')


            self.saveLastFile(fname)

            # бежим по линиям
            sch = 0
            for line in fd:
                sch = sch + 1
                _line = line
                line = line.replace('\n', '')
                line = line.replace('0x', '')

                # пропускаем вторую
                if line == '':
                    continue

                # берем второе число
                line = line.split('\t')
                line = line[1]
                line = int(line, 16)

                # первые два байта - адрес регистра
                regAddr = line >> 8

                # последний байт - значение регистра
                regVal = line & 0xFF

                self.dev.write(regAddr, regVal)

            fd.seek(0)

            # проверяем, что все было записано

            for line in fd:

                _line = line
                line = line.replace('\n', '')
                line = line.replace('0x', '')

                if line == '':
                    continue

                line = line.split('\t')
                line = line[1]
                line = int(line, 16)

                regAddr = line >> 8
                regVal = line & 0xFF

                skip = [0x0, 0x1ffd, 0x1ffe, 0x1fff, 0x006]
                if regAddr in skip:
                    continue

                tmp = self.dev.read(regAddr)
                if tmp != regVal:
                    self.writeLog('Предупреждение: Регистр ' + hex(regAddr) + ' после записи значения ' + hex(
                        regVal) + ' равен ' + hex(tmp) + ' Строка: ' + str(sch))
                    flg = False  # в ходе записи была ошибка

            fd.close()



            # в конце заново читаем статус после настройки
            self.clearStatus()

            if flg:
                self.writeLog('Запись прошла без ошибок!')


            self.writeLog('Запись файла \'' + fname + '\' завершена.')

        except Exception as e:
            if sch:
                self.writeLog('Неверный файл! ' + "Ошибка: '" + str(e) + "' на строке " + str(sch))  # ошибка в файле
            else:
                self.writeLog('Неверный файл! ' + "Ошибка: " + str(e)) # ошибка в пути файла
            return None


        return [regs, vals]


    # кнопка выбора файла
    def selectFilePushButtonClicked(self):
        filt = "Text(*.txt);;All(*.*)"  # фильтры файлов - все и текстовые
        self.fileLineEdit.setText(QFileDialog.getOpenFileName(filter=filt)[0])

    # Ручная запись в регистр
    def regWritePushButtonClicked(self):

        try:
            addr = int(self.regAddrLineEdit.text(), 16)
            val = int(self.regValLineEdit.text(), 16)
            self.dev.write(addr, val)
            self.writeLog("В регистр  " + hex(addr) + " записано  " + hex(val))
        except:
           self.writeLog('Неверный формат!')

    # ручное чтение из регистра
    def regReadPushButtonClicked(self):
        try:
            addr = int(self.regAddrLineEdit.text(), 16)
            val = self.dev.read(addr)
            self.regValLineEdit.setText(hex(val).replace('0x', ''))
            self.writeLog("Из регистра " + hex(addr) + " считано " + hex(val))
        except:
            self.writeLog('Неверный формат!')


    # обработчик записи файла
    def writeFile(self):
        fname = self.fileLineEdit.text()
        self.parseFile(fname)

    # --- Дальше вроде все понятно

    def showMsg(self, text):
        QtWidgets.QMessageBox.information(self, 'Сообщение', text)

    def showErr(self, text):
        QtWidgets.QMessageBox.critical(self, 'Ошибка!', text)

    def initSlots(self):
        self.clearLogPushButton.clicked.connect(self.clearLog)
        self.selectFilePushButton.clicked.connect(self.selectFilePushButtonClicked)
        self.writeFilePushButton.clicked.connect(self.writeFile)
        self.regWritePushButton.clicked.connect(self.regWritePushButtonClicked)
        self.regReadPushButton.clicked.connect(self.regReadPushButtonClicked)
        self.readPllPushButton.clicked.connect(self.checkStatus)
        self.clearPllPushButton.clicked.connect(self.clearStatus)
        self.autoStatCheckBox.stateChanged.connect(self.autoStatCheckBoxHandle)
        self.recPushButton.clicked.connect(self.recPushButtonClicked)
        self.resetPushButton.clicked.connect(self.resetPushButtonClicked)

    def clearLog(self):
        self.logTextEdit.setText('')

    def writeLog(self, msg):

        old_text = self.logTextEdit.toPlainText()

        msg = datetime.now().strftime('%H:%M:%S') + ' :: ' + msg

        if old_text == '':
            self.logTextEdit.setText(msg)
        else:
            self.logTextEdit.setText(old_text + '\n' + msg)


        self.logTextEdit.moveCursor(QtGui.QTextCursor.End)