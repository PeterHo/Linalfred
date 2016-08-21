# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QTextCursor
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

    def setText(self, text):
        self.setPlainText(text)
        c = QTextCursor(self.document())
        c.setPosition(len(text))
        self.setTextCursor(c)

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        key = event.key()
        alt, ctrl, win = False, False, False
        if modifiers & Qt.AltModifier:
            alt = True
        if modifiers & Qt.ControlModifier:
            ctrl = True
        if modifiers & Qt.MetaModifier:
            win = True

        if alt or ctrl or win:
            index = self.dlg.listBox.getItemIndexByShortcut(modifiers, key)
            if index != -1:
                if self.dlg.listBox.enterItem(index):
                    self.dlg.closeDlg()
                return

        if key == Qt.Key_Enter or key == Qt.Key_Return:
            self.dlg.onEnterCurItem()
            return
        elif key == Qt.Key_Up or (ctrl and key == Qt.Key_K):
            if self.dlg.listBox.getCurCount() > 0:
                self.dlg.listBox.selPreItem()
                pass
            else:
                # TODO 显示切换历史命令
                pass
        elif key == Qt.Key_Down or (ctrl and key == Qt.Key_J):
            if self.dlg.listBox.getCurCount() > 0:
                self.dlg.listBox.selNextItem()
            else:
                # TODO 显示切换历史命令
                pass
        elif key == Qt.Key_Tab:
            # 如果有列表项并且命令中无空格,则补全
            if self.dlg.listBox.getCurCount() > 0:
                if ' ' not in self.toPlainText():
                    self.setText(self.dlg.listBox.getCurItemKeyword() + " ")
        else:
            super().keyPressEvent(event)

    def clearEditBox(self):
        self.clear()
