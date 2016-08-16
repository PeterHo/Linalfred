# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Widget(object):
    def setupUi(self, Widget):
        Widget.setObjectName("Widget")
        Widget.resize(700, 117)
        Widget.setMinimumSize(QtCore.QSize(700, 0))
        Widget.setMaximumSize(QtCore.QSize(700, 117))
        font = QtGui.QFont()
        font.setPointSize(60)
        Widget.setFont(font)
        Widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gridLayout = QtWidgets.QGridLayout(Widget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(999999, 999999))
        font = QtGui.QFont()
        font.setPointSize(70)
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setContentsMargins(11, 11, 11, 11)
        self.formLayout.setSpacing(6)
        self.formLayout.setObjectName("formLayout")
        self.gridLayout.addWidget(self.groupBox, 0, 1, 1, 1)

        self.retranslateUi(Widget)
        QtCore.QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        _translate = QtCore.QCoreApplication.translate
        Widget.setWindowTitle(_translate("Widget", "Widget"))

