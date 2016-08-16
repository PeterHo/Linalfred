# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'doublelistitem.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DoubleListItem(object):
    def setupUi(self, DoubleListItem):
        DoubleListItem.setObjectName("DoubleListItem")
        DoubleListItem.resize(662, 51)
        self.text = QtWidgets.QLabel(DoubleListItem)
        self.text.setGeometry(QtCore.QRect(52, -2, 551, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.text.setFont(font)
        self.text.setObjectName("text")
        self.cmd = QtWidgets.QLabel(DoubleListItem)
        self.cmd.setGeometry(QtCore.QRect(607, -2, 41, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cmd.setFont(font)
        self.cmd.setText("")
        self.cmd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cmd.setObjectName("cmd")
        self.icon = QtWidgets.QLabel(DoubleListItem)
        self.icon.setGeometry(QtCore.QRect(0, -2, 51, 53))
        self.icon.setText("")
        self.icon.setObjectName("icon")
        self.subtext = QtWidgets.QLabel(DoubleListItem)
        self.subtext.setGeometry(QtCore.QRect(52, 25, 549, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.subtext.setFont(font)
        self.subtext.setObjectName("subtext")

        self.retranslateUi(DoubleListItem)
        QtCore.QMetaObject.connectSlotsByName(DoubleListItem)

    def retranslateUi(self, DoubleListItem):
        _translate = QtCore.QCoreApplication.translate
        DoubleListItem.setWindowTitle(_translate("DoubleListItem", "Form"))
        self.text.setText(_translate("DoubleListItem", "TextLabel"))
        self.subtext.setText(_translate("DoubleListItem", "TextLabelg"))

