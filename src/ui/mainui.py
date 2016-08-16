# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import getAllApps
from ui.config import Cfg
from ui.designer.widget import Ui_Widget
from ui.listItem import ListItem
from ui.plaintext import PlainText
from ui.theme import Theme
from ui.thread import WidgetThread

__author__ = 'peter'


class MainUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.mutexPaint = QMutex()
        self.mutexThread = QMutex()

        self.theme = Theme("Classic")

        self.plainTextEdit = PlainText(self)
        self.plainTextEdit.setObjectName("plainTextEdit")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setMinimumSize(self.theme.dimensions)
        self.plainTextEdit.setMaximumSize(QSize(2048, self.theme.dimensions.height()))

        font2 = QFont()
        font2.setPointSize(self.theme.fontSize)

        self.plainTextEdit.setFont(font2)
        self.plainTextEdit.setFocusPolicy(Qt.StrongFocus)
        self.plainTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.plainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.ui.formLayout.setWidget(0, QFormLayout.SpanningRole, self.plainTextEdit)

        self.listWidget = QListWidget(self.ui.groupBox)
        self.plainTextEdit.listWidget = self.listWidget
        self.listWidget.setObjectName("listWidget")

        font1 = QFont()
        font1.setPointSize(20)

        self.listWidget.setFont(font1)
        self.listWidget.setFocusPolicy(Qt.NoFocus)

        self.ui.formLayout.setWidget(1, QFormLayout.SpanningRole, self.listWidget)

        self.listWidget.setStyleSheet(self.theme.listWidgetStylesheet)
        self.listWidget.setIconSize(QSize(Cfg.iconSize, Cfg.iconSize))
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setMinimumHeight(1024)
        self.listWidget.hide()

        self.ui.groupBox.setStyleSheet(self.theme.groupBoxStylesheet)

        wndShadow = QGraphicsDropShadowEffect()
        wndShadow.setBlurRadius(self.theme.blurRadius)
        wndShadow.setColor(self.theme.shadowColor)
        wndShadow.setOffset(self.theme.shadowOffset)
        self.ui.groupBox.setGraphicsEffect(wndShadow)

        self.plainTextEdit.setStyleSheet(self.theme.plainTextEditStylesheet)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)

        self.plainTextEdit.textChanged.connect(self.onCmd)
        self.listWidget.currentRowChanged.connect(self.onSetOne)
        self.listWidget.itemPressed.connect(self.onEnterCurItem)

        self.plainTextEdit.setFocus()

        self.setGeometry(self.x(), self.y(), self.theme.beginHeight, self.width())

        self.apps = getAllApps()

        self.center()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            print("return")
        elif e.key() == Qt.Key_Escape:
            # self.close()
            QCoreApplication.instance().quit()

    def onCmd(self):
        cmd = self.plainTextEdit.toPlainText()
        if cmd:
            t = WidgetThread(self)
            t.finishSignal.connect(self.mutexShowList)
            t.start()
        else:
            self.clearList()

    def onSetOne(self):
        if self.listWidget.currentRow() == -1:
            self.listWidget.setCurrentRow(0)

    def onEnterCurItem(self):
        pass

    def showList(self, ls):
        self.listWidget.clear()
        if not ls:
            self.clearList()
            return
        listSize = min(len(ls), Cfg.maxListSize)
        printSize = min(len(ls), Cfg.maxPrintSize)
        listWidgetHeight = Cfg.rowSize * printSize
        mainUISizeHeight = listWidgetHeight + self.theme.beginHeight
        self.listWidget.show()
        self.listWidget.setMaximumHeight(listWidgetHeight)
        self.listWidget.setGeometry(self.listWidget.x(),
                                    self.theme.listWidgetY,
                                    self.listWidget.width(),
                                    listWidgetHeight)
        self.setMaximumHeight(mainUISizeHeight)
        self.setMinimumHeight(mainUISizeHeight)
        self.setGeometry(self.x(), self.y(), mainUISizeHeight, self.width())

        for i in range(listSize):
            listItem = ListItem(ls[i].iconName, ls[i].name, "Alt+" + str(i + 1))
            listWidgetItem = QListWidgetItem(self.listWidget)
            listWidgetItem.setSizeHint(QSize(listItem.width(), listItem.height()))
            self.listWidget.addItem(listWidgetItem)
            self.listWidget.setItemWidget(listWidgetItem, listItem)
        self.listWidget.setCurrentRow(0)
        self.listWidget.setGeometry(self.listWidget.x(),
                                    self.theme.listWidgetY,
                                    self.listWidget.width(),
                                    listWidgetHeight)

    def clearList(self):
        self.listWidget.clear()
        self.listWidget.hide()
        self.setMaximumHeight(self.theme.beginHeight)
        self.setMinimumHeight(self.theme.beginHeight)
        self.setGeometry(self.x(), self.y(), self.theme.beginHeight, self.width())

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
        y = (deskY - Cfg.beginHeight - Cfg.rowSize * (Cfg.maxPrintSize - 1)) * 0.4
        self.move(x, y)
