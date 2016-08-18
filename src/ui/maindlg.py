# coding=utf-8
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import getAllApps
from cmd import CmdType
from config import Cfg
from shortcut import ListShortcut
from ui.maineditbox import MainEditBox
from ui.mainlistbox import MainListBox
from ui.theme import Theme
from ui.thread import DlgThread

__author__ = 'peter'


class MainDlg(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = uic.loadUi('ui/designer/widget.ui', self)

        self.mutexPaint = QMutex()
        self.mutexThread = QMutex()

        self.theme = Theme()

        self.editBox = MainEditBox(self, self)
        self.editBox.setObjectName("mainEditBox")
        self.editBox.setSize()
        self.editBox.setEditBoxFont()
        self.editBox.setOtherStyles()

        self.listBox = MainListBox(self.ui.groupBox, self)
        self.listBox.setObjectName("mainListBox")
        self.listBox.setSize()
        self.listBox.setListBoxFont()
        self.listBox.setOtherStyles()
        self.listBox.hide()

        self.ui.formLayout.setWidget(0, QFormLayout.SpanningRole, self.editBox)
        self.ui.formLayout.setWidget(1, QFormLayout.SpanningRole, self.listBox)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(self.theme.blurRadius)
        shadow.setColor(self.theme.shadowColor)
        shadow.setOffset(self.theme.shadowOffset)
        self.ui.groupBox.setGraphicsEffect(shadow)
        self.ui.groupBox.setStyleSheet(self.theme.groupBoxStylesheet)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        self.editBox.textChanged.connect(self.onCmdChanged)
        self.listBox.currentRowChanged.connect(self.onSetOne)
        self.listBox.itemPressed.connect(self.onEnterCurItem)

        self.editBox.setFocus()

        self.center()

    def show(self):
        print("get all apps")
        self.apps = getAllApps()
        self.clearList()
        self.editBox.clearEditBox()
        super().show()

    def closeDlg(self):
        self.clearList()
        self.editBox.clearEditBox()
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            print("return")
        elif e.key() == Qt.Key_Escape:
            self.closeDlg()
        else:
            super().keyPressEvent(e)

    def onCmdChanged(self):
        cmd = self.editBox.toPlainText()
        if cmd:
            t = DlgThread(self)
            t.finishSignal.connect(self.mutexShowList)
            t.start()
        else:
            self.clearList()

    def onSetOne(self):
        if self.listBox.currentRow() == -1:
            self.listBox.setCurrentRow(0)

    def onEnterCurItem(self):
        self.listBox.enterCurItem()
        self.closeDlg()

    def showList(self, cmds):
        self.listBox.clear()
        if not cmds:
            self.clearList()
            return
        rowCnt = min(len(cmds), Cfg.UI.maxListSize)
        listBoxHeight = self.theme.rowSize * rowCnt
        dlgHeight = listBoxHeight + self.theme.dlgHeight
        self.listBox.show()

        for i in range(rowCnt):
            cmds[i].shortcutKey = ListShortcut.getShortcutKey(i)
            cmds[i].modifier = ListShortcut.getModifier(i)
            self.listBox.addCmdItem(cmds[i], ListShortcut.getShortcutText(i))
        self.listBox.setCurrentRow(0)
        self.listBox.setMaximumHeight(listBoxHeight)
        self.listBox.setGeometry(self.listBox.x(), self.theme.listY,
                                 self.listBox.width(), listBoxHeight)
        self.setMaximumHeight(dlgHeight)
        self.setMinimumHeight(dlgHeight)
        self.setGeometry(self.x(), self.y(), dlgHeight, self.width())

    def clearList(self):
        self.listBox.clear()
        self.listBox.hide()
        self.setMaximumHeight(self.theme.dlgHeight)
        self.setMinimumHeight(self.theme.dlgHeight)
        self.setGeometry(self.x(), self.y(), self.theme.dlgHeight, self.width())

    def mutexShowList(self, ls):
        self.mutexPaint.lock()
        self.showList(ls)
        self.mutexPaint.unlock()

    def center(self):
        desktop = QApplication.desktop()
        deskRect = desktop.screenGeometry(desktop.screenNumber(QCursor.pos()))
        deskX = deskRect.width()
        deskY = deskRect.height()
        x = deskX / 2 - self.width() / 2 + deskRect.left()
        y = (deskY - self.theme.dlgHeight - self.theme.rowSize * (Cfg.UI.maxListSize - 1)) * 0.4
        self.move(x, y)
