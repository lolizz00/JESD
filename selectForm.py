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

# формочка для выбора устройства
# высвечивается при старте


class SW(QtWidgets.QWidget, Ui_selectForm):


    selectSignal = pyqtSignal(int)

    def __init__(self):
        super(SW, self).__init__()
        self.setupUi(self)
        self.initSlots()
        self.refrDevListPushButtonClicked()  #  сразу обновляем
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint) # вешаем поверх всех оконо

    def initSlots(self):
        self.refrDevListPushButton.clicked.connect(self.refrDevListPushButtonClicked)
        self.connectDevPushButton.clicked.connect(self.connectDevPushButtonClicked)
        self.LEDDevPushButton.clicked.connect(self.LEDDevPushButtonClicked)


    def showErr(self, text):
        QtWidgets.QMessageBox.critical(self, 'Ошибка!', text)


    # подключение
    def connectDevPushButtonClicked(self):
        ind = self.devListComboBox.currentIndex() # берем индекс
        if ind == -1:
            self.showErr('Нет доступных устройств!')
            return

        try:
            dev = JESD()
            dev.connect(ind) # подключаемся по индексу, что бы проверить живое ли устройство
            dev = None # отключаемся, все нормально
            self.selectSignal.emit(ind) # передаем номер главному окну
            self.hide() # скрываем окно
        except  Exception as e:
            self.showErr('Ошибка при подключении: ' + str(e))
            return


    # просят помигать
    def LEDDevPushButtonClicked(self):
        ind = self.devListComboBox.currentIndex() # выбираем устройство
        if ind == -1:
            self.showErr('Нет доступных устройств!')
            return

        try:
            dev = JESD() # подключаемся
            dev.connect(ind)
            dev.LEDBlink() # мигаем
        except:
            self.showErr('Ошибка: ' + str(e))


    # обновление списка всех устройств
    def refrDevListPushButtonClicked(self):
            dev = JESD()
            lst = dev.getListStr()
            self.devListComboBox.clear()
            self.devListComboBox.addItems(lst)