from PyQt5 import QtCore, QtGui, QtWidgets
from mw import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon
from datetime import datetime

from JESDdriver import JESD

class MW(QtWidgets.QMainWindow, Ui_MainWindow):


    def refrDevListPushButtonClicked(self):
        lst = self.dev.getListStr()
        self.devListComboBox.clear()
        self.devListComboBox.addItems(lst)


    def clearStatus(self):
        self.dev.clearStatus()

    def checkStatus(self):
        stat1 = self.dev.checkStatus(1)
        self.pll1Label.setText(stat1)
        if stat1 != "OK":
            self.pll1Label.setStyleSheet("color: red")
        else:
            self.pll1Label.setStyleSheet("color: black")

        stat2 = self.dev.checkStatus(2)
        self.pll2Label.setText(stat2)
        if stat2 != "OK":
            self.pll2Label.setStyleSheet("color: red")
        else:
            self.pll2Label.setStyleSheet("color: black")


    def connectDevPushButtonClicked(self):
        id = int(self.devListComboBox.currentIndex())

        if id == -1:
            self.showErr('Нет доступных устройств!')
            return

        info = None
        try:
            info = self.dev.connect(id)
        except Exception as e:
            self.showErr('Ошибка при подключении: ' + str(e))
            self.writeLog('Ошибка при подключении: ' + str(e))
            return

        self.writeLog('Подлючено.')
        self.writeLog('Product ID:' + info)
        self.disableAll(False)

    def disconnectDevPushButtonClicked(self):
        self.dev.disconnect()
        self.writeLog('Отключено.')
        self.disableAll(True)

    def LEDDevPushButtonClicked(self):
        self.dev.LEDBlink()

    def __init__(self):
        super(MW, self).__init__()
        self.setupUi(self)
        self.setCentralWidget(self.cw)
        self.initSlots()
        self.dev = JESD()



        self.refrDevListPushButtonClicked()

    def parseFile(self, fname):


        regs = []
        vals = []

        self.dev.reset()
        self.dev.enableWrite()
        self.dev.set4Wire()

        try:
            fd = open(fname, 'r')

            flg = True

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


                # хз, нв всякий случай
                if regAddr & 0x8000:
                    self.writeLog('Пропускаем чтение из регистра ' + hex(regAddr))
                    continue

                # пропускаем сбросы
                skip = [0x0, 0x1ffd, 0x1ffe, 0x1fff, 0x006]
                if regAddr in skip:
                    continue

                self.dev.write(regAddr, regVal)
                tmp = self.dev.read(regAddr)

                if tmp != regVal:
                    self.writeLog('Предупреждение: Регистр ' + hex(regAddr) + ' после записи значения ' + hex(regVal) + ' равен ' + hex(tmp))
                    self.writeLog('Строка: \"' + _line.replace('\n', '') + "\"")
                    flg = False

            fd.close()

            if flg:
                self.writeLog('Запись прошла без ошибок!')

            self.writeLog('Запись завершена.')

        except:
            self.writeLog('Неверный файл!')
            return None


        return [regs, vals]

    def selectFilePushButtonClicked(self):
        self.fileLineEdit.setText(QFileDialog.getOpenFileName()[0])

    def disableAll(self, state):
        state = not state

        self.writeFilePushButton.setEnabled(state)
        self.regReadPushButton.setEnabled(state)
        self.regWritePushButton.setEnabled(state)
        self.disconnectDevPushButton.setEnabled(state)
        self.LEDDevPushButton.setEnabled(state)
        self.connectDevPushButton.setEnabled(not state)
        self.clearPllPushButton.setEnabled(state)
        self.readPllPushButton.setEnabled(state)


    def regWritePushButtonClicked(self):

        try:
            addr = int(self.regAddrLineEdit.text(), 16)
            val = int(self.regValLineEdit.text(), 16)
            self.dev.write(addr, val)
            self.writeLog("Успешно записано.")
        except:
           self.writeLog('Неверный формат!')

    def regReadPushButtonClicked(self):
        try:
            addr = int(self.regAddrLineEdit.text(), 16)
            val = self.dev.read(addr)
            self.regValLineEdit.setText(hex(val).replace('0x', ''))
            self.writeLog("Успешно считано.")
        except:
            self.writeLog('Неверный формат!')


    def writeFile(self):
        fname = self.fileLineEdit.text()
        self.parseFile(fname)


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


        self.refrDevListPushButton.clicked.connect(self.refrDevListPushButtonClicked)
        self.connectDevPushButton.clicked.connect(self.connectDevPushButtonClicked)
        self.disconnectDevPushButton.clicked.connect(self.disconnectDevPushButtonClicked)
        self.LEDDevPushButton.clicked.connect(self.LEDDevPushButtonClicked)


        self.readPllPushButton.clicked.connect(self.checkStatus)
        self.clearPllPushButton.clicked.connect(self.clearStatus)



    def clearLog(self):
        self.logTextEdit.setText('')

    def writeLog(self, msg):

        old_text = self.logTextEdit.toPlainText()

        msg = datetime.now().strftime('%H:%M:%S') + ' :: ' + msg

        if old_text == '':
            self.logTextEdit.setText(msg)
        else:
            self.logTextEdit.setText(old_text + '\n' + msg)