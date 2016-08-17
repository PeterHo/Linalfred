# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

__author__ = 'peter'


class MainEditBox(QPlainTextEdit):
    def __init__(self, parent, mainDlg):
        super().__init__(parent)
        self.dlg = mainDlg

    def setSize(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(self.dlg.theme.editBoxSize)
        self.setMaximumSize(QSize(2048, self.dlg.theme.editBoxSize.height()))

    def setEditBoxFont(self):
        font = QFont()
        font.setPointSize(self.dlg.theme.editBoxFontSize)
        self.setFont(font)

    def setOtherStyles(self):
        self.setStyleSheet(self.dlg.theme.editBoxStylesheet)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
