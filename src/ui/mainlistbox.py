# coding=utf-8
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

__author__ = 'peter'


class ListItem(QWidget):
    def __init__(self, parent, cmd, shortcut):
        super().__init__(parent)
        self.ui = uic.loadUi('ui/designer/listitem.ui', self)
        self.dlg = parent
        self.cmd = cmd

        self.ui.shortcut.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")
        fm = QFontMetrics(self.ui.text.font())
        self.ui.text.setText(fm.elidedText(self.cmd.name, Qt.ElideRight, self.ui.text.width()))
        self.ui.shortcut.setText(shortcut)
        if not self.cmd.iconName:
            self.cmd.iconName = self.dlg.theme.defaultIcon
        qIcon = QIcon(self.cmd.iconName)
        p = qIcon.pixmap(QSize(self.dlg.theme.iconSize, self.dlg.theme.iconSize))
        self.ui.icon.setPixmap(p)


class MainListBox(QListWidget):
    def __init__(self, parent, mainDlg):
        super().__init__(parent)
        self.dlg = mainDlg
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        row = self.indexAt(event.pos()).row()
        self.setCurrentRow(row)

    def setSize(self):
        self.setMinimumHeight(1024)

    def setListBoxFont(self):
        font = QFont()
        font.setPointSize(20)
        self.setFont(font)

    def setOtherStyles(self):
        self.setIconSize(QSize(self.dlg.theme.iconSize, self.dlg.theme.iconSize))
        self.setStyleSheet(self.dlg.theme.listStylesheet)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def addCmdItem(self, cmd, shortcut):
        listItem = ListItem(self.dlg, cmd, shortcut)
        listWidgetItem = QListWidgetItem(self)
        listWidgetItem.setSizeHint(QSize(listItem.width(), listItem.height()))
        self.addItem(listWidgetItem)
        self.setItemWidget(listWidgetItem, listItem)

    def selPreItem(self):
        self.setCurrentRow((self.currentRow() + self.count() - 1) % self.count())

    def selNextItem(self):
        self.setCurrentRow((self.currentRow() + 1) % self.count())
