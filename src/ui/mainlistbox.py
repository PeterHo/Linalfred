# coding=utf-8
import os

from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from cmd import CmdType
from config import Cfg

__author__ = 'peter'


class ListItem(QWidget):
    def __init__(self, parent, cmd, shortcut):
        super().__init__(parent)
        self.ui = uic.loadUi(Cfg.srcPath + 'ui/designer/listitem.ui', self)
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
    def __init__(self, parent, dlg):
        super().__init__(parent)
        self.ui = uic.loadUi(Cfg.srcPath + 'ui/designer/doublelistitem.ui', self)
        self.dlg = dlg
        self.cmd = None

        self.ui.subtext.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")
        self.ui.shortcut.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")

    def setInfo(self, cmd, shortcut):
        self.cmd = cmd
        fm = QFontMetrics(self.ui.text.font())
        self.ui.text.setText(fm.elidedText(self.cmd.name, Qt.ElideRight, self.ui.text.width()))
        self.ui.subtext.setText(fm.elidedText(self.cmd.getDesc(), Qt.ElideLeft, self.ui.text.width()))
        self.ui.shortcut.setText(shortcut)

        if not self.cmd.iconName:
            self.cmd.iconName = self.dlg.theme.getDefaultIcon(self.cmd.type)
        if '/' not in self.cmd.iconName:
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
        self.itemList = []
        self.curCount = Cfg.getInt('ui', 'maxListSize')
        for i in range(self.curCount):
            item = DoubleListItem(self, self.dlg)
            self.itemList.append(item)
            listWidgetItem = QListWidgetItem(self)
            listWidgetItem.setSizeHint(QSize(item.width(), item.height()))
            self.addItem(listWidgetItem)
            self.setItemWidget(listWidgetItem, item)

    def setCurCount(self, count):
        self.curCount = count

    def getCurCount(self):
        return self.curCount

    def mouseMoveEvent(self, event):
        row = self.indexAt(event.pos()).row()
        if row >= self.curCount:
            row = self.curCount - 1
        self.setCurrentRow(row)

    def setSize(self):
        self.setMinimumHeight(1024)

    def setListBoxFont(self):
        font = QFont()
        font.setPointSize(self.dlg.theme.listFontSize)
        self.setFont(font)

    def setOtherStyles(self):
        self.setIconSize(QSize(self.dlg.theme.iconSize, self.dlg.theme.iconSize))
        self.setStyleSheet(self.dlg.theme.listStylesheet)
        self.setFocusPolicy(Qt.NoFocus)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setCmdItem(self, index, cmd, shortcut):
        self.itemList[index].setInfo(cmd, shortcut)

    def selPreItem(self):
        self.setCurrentRow((self.currentRow() + self.curCount - 1) % self.curCount)

    def selNextItem(self):
        self.setCurrentRow((self.currentRow() + 1) % self.curCount)

    def getItem(self, index):
        listWidgetItem = self.item(index)
        return self.itemWidget(listWidgetItem)

    def getItemText(self, index):
        listWidgetItem = self.item(index)
        return listWidgetItem.text

    def showItem(self, index):
        self.itemList[index].show()

    def hideItem(self, index):
        self.itemList[index].hide()

    def enterItem(self, index):
        if index >= self.curCount or index < 0:
            return False
        item = self.getItem(index)
        return item.cmd.exec(self.dlg.editBox.toPlainText())

    def enterCurItem(self):
        return self.enterItem(self.currentRow())

    def getCurItem(self):
        return self.getItem(self.currentRow())

    def getCurItemCmd(self):
        return self.getCurItem().cmd

    def getCurItemKeyword(self):
        return self.getCurItemCmd().keyword

    def getItemIndexByShortcut(self, modifiers, key):
        for i in range(self.curCount):
            item = self.getItem(i)
            if item.cmd.modifier & modifiers and item.cmd.shortcutKey == key:
                return i

        return -1

    # 补全
    def complement(self, text):
        return self.getCurItemCmd().complement(text)

