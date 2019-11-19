from PyQt5 import QtCore, QtGui, QtWidgets
from selectformui import Ui_selectForm
from version import version_logo
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon
from datetime import datetime

from JESDdriver import JESD

class SW(QtWidgets.QWidget, Ui_selectForm):


    selectSignal = pyqtSignal(int)

    def __init__(self):
        super(SW, self).__init__()
        self.setupUi(self)
        self.initSlots()
        self.refrDevListPushButtonClicked()
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

    def initSlots(self):
        self.refrDevListPushButton.clicked.connect(self.refrDevListPushButtonClicked)
        self.connectDevPushButton.clicked.connect(self.connectDevPushButtonClicked)
        self.LEDDevPushButton.clicked.connect(self.LEDDevPushButtonClicked)


    def showErr(self, text):
        QtWidgets.QMessageBox.critical(self, 'Ошибка!', text)

    def connectDevPushButtonClicked(self):
        ind = self.devListComboBox.currentIndex()
        if ind == -1:
            self.showErr('Нет доступных устройств!')
            return

        try:
            dev = JESD()
            dev.connect(ind)
            dev = None
            self.selectSignal.emit(ind)
            self.hide()
        except  Exception as e:
            self.showErr('Ошибка при подключении: ' + str(e))
            return



    def LEDDevPushButtonClicked(self):
        ind = self.devListComboBox.currentIndex()
        if ind == -1:
            self.showErr('Нет доступных устройств!')
            return

        try:
            dev = JESD()
            dev.connect(ind)
            dev.LEDBlink()
        except:
            self.showErr('Ошибка: ' + str(e))

    def refrDevListPushButtonClicked(self):
            dev = JESD()
            lst = dev.getListStr()
            self.devListComboBox.clear()
            self.devListComboBox.addItems(lst)