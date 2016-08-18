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

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        key = event.key()
        if modifiers & Qt.AltModifier:
            pass
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.dlg.onEnterCurItem()
            return
        elif key == Qt.Key_Up:
            if self.dlg.listBox.count() > 0:
                self.dlg.listBox.selPreItem()
                pass
            else:
                # TODO 显示切换历史命令
                pass
        elif key == Qt.Key_Down:
            if self.dlg.listBox.count() > 0:
                self.dlg.listBox.selNextItem()
            else:
                # TODO 显示切换历史命令
                pass
        else:
            super().keyPressEvent(event)

