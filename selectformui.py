# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'H:\JESD\selectform.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_selectForm(object):
    def setupUi(self, selectForm):
        selectForm.setObjectName("selectForm")
        selectForm.resize(450, 100)
        selectForm.setMinimumSize(QtCore.QSize(450, 100))
        selectForm.setMaximumSize(QtCore.QSize(450, 100))
        self.layoutWidget = QtWidgets.QWidget(selectForm)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 0, 371, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setMinimumSize(QtCore.QSize(115, 0))
        self.label_6.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.devListComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.devListComboBox.setObjectName("devListComboBox")
        self.horizontalLayout_2.addWidget(self.devListComboBox)
        self.refrDevListPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.refrDevListPushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.refrDevListPushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refrDevListPushButton.setIcon(icon)
        self.refrDevListPushButton.setObjectName("refrDevListPushButton")
        self.horizontalLayout_2.addWidget(self.refrDevListPushButton)
        self.LEDDevPushButton = QtWidgets.QPushButton(selectForm)
        self.LEDDevPushButton.setEnabled(True)
        self.LEDDevPushButton.setGeometry(QtCore.QRect(230, 60, 121, 31))
        self.LEDDevPushButton.setObjectName("LEDDevPushButton")
        self.connectDevPushButton = QtWidgets.QPushButton(selectForm)
        self.connectDevPushButton.setGeometry(QtCore.QRect(140, 60, 84, 31))
        self.connectDevPushButton.setObjectName("connectDevPushButton")

        self.retranslateUi(selectForm)
        QtCore.QMetaObject.connectSlotsByName(selectForm)

    def retranslateUi(self, selectForm):
        _translate = QtCore.QCoreApplication.translate
        selectForm.setWindowTitle(_translate("selectForm", "JESD"))
        self.label_6.setText(_translate("selectForm", "Список устройств:"))
        self.LEDDevPushButton.setText(_translate("selectForm", "Мигнуть светодиодом"))
        self.connectDevPushButton.setText(_translate("selectForm", "Подключиться"))


