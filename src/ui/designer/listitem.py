# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listitem.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ListItem(object):
    def setupUi(self, ListItem):
        ListItem.setObjectName("ListItem")
        ListItem.resize(662, 51)
        self.icon = QtWidgets.QLabel(ListItem)
        self.icon.setGeometry(QtCore.QRect(0, 0, 51, 51))
        self.icon.setText("")
        self.icon.setObjectName("icon")
        self.text = QtWidgets.QLabel(ListItem)
        self.text.setGeometry(QtCore.QRect(52, -3, 551, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.text.setFont(font)
        self.text.setObjectName("text")
        self.cmd = QtWidgets.QLabel(ListItem)
        self.cmd.setGeometry(QtCore.QRect(607, -2, 41, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cmd.setFont(font)
        self.cmd.setText("")
        self.cmd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cmd.setObjectName("cmd")

        self.retranslateUi(ListItem)
        QtCore.QMetaObject.connectSlotsByName(ListItem)

    def retranslateUi(self, ListItem):
        _translate = QtCore.QCoreApplication.translate
        ListItem.setWindowTitle(_translate("ListItem", "Form"))
        self.text.setText(_translate("ListItem", "TextLabel"))

