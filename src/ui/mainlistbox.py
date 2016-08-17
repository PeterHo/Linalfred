# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.designer.listitem import Ui_ListItem

__author__ = 'peter'


class ListItem(QWidget):
    def __init__(self, parent, icon, text, cmd):
        super().__init__(parent)
        self.ui = Ui_ListItem()
        self.ui.setupUi(self)

        self.dlg = parent

        self.ui.cmd.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")
        fm = QFontMetrics(self.ui.text.font())
        self.ui.text.setText(fm.elidedText(text, Qt.ElideRight, self.ui.text.width()))
        self.ui.cmd.setText(cmd)
        if icon:
            qIcon = QIcon(icon)
        else:
            qIcon = QIcon(self.dlg.theme.defaultIcon)
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

    def addAppItem(self, iconName, name, cmd):
        listItem = ListItem(self.dlg, iconName, name, cmd)
        listWidgetItem = QListWidgetItem(self)
        listWidgetItem.setSizeHint(QSize(listItem.width(), listItem.height()))
        self.addItem(listWidgetItem)
        self.setItemWidget(listWidgetItem, listItem)
