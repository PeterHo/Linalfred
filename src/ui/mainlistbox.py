# coding=utf-8
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cmd import CmdType

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


class DoubleListItem(QWidget):
    def __init__(self, parent, cmd, shortcut):
        super().__init__(parent)
        self.ui = uic.loadUi('ui/designer/doublelistitem.ui', self)
        self.dlg = parent
        self.cmd = cmd

        self.ui.subtext.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")
        self.ui.shortcut.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")
        fm = QFontMetrics(self.ui.text.font())
        self.ui.text.setText(fm.elidedText(self.cmd.name, Qt.ElideRight, self.ui.text.width()))
        self.ui.subtext.setText(fm.elidedText(self.cmd.executable, Qt.ElideRight, self.ui.text.width()))
        self.ui.shortcut.setText(shortcut)
        if not self.cmd.iconName:
            self.cmd.iconName = self.dlg.theme.getDefaultIcon(self.cmd.type)
        if '/' not in self.cmd.iconName:
            print("from theme")
            qIcon = QIcon.fromTheme(self.cmd.iconName)
        else:
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
        listItem = DoubleListItem(self.dlg, cmd, shortcut)
        listWidgetItem = QListWidgetItem(self)
        listWidgetItem.setSizeHint(QSize(listItem.width(), listItem.height()))
        self.addItem(listWidgetItem)
        self.setItemWidget(listWidgetItem, listItem)

    def selPreItem(self):
        self.setCurrentRow((self.currentRow() + self.count() - 1) % self.count())

    def selNextItem(self):
        self.setCurrentRow((self.currentRow() + 1) % self.count())

    def getItem(self, index):
        listWidgetItem = self.item(index)
        return self.itemWidget(listWidgetItem)

    def enterItem(self, index):
        if index >= self.count() or index < 0:
            return
        item = self.getItem(index)
        if item.cmd.type == CmdType.app:
            print(item.cmd.executable)
            QProcess.startDetached(item.cmd.executable)
        elif item.cmd.type == CmdType.file:
            QProcess.startDetached('xdg-open', [item.cmd.executable])

    def enterCurItem(self):
        self.enterItem(self.currentRow())

    def getItemIndexByShortcut(self, modifiers, key):
        for i in range(self.count()):
            item = self.getItem(i)
            if item.cmd.modifier & modifiers and item.cmd.shortcutKey == key:
                return i

        return -1
