# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from app import getAllApps
from ui.config import Cfg
from ui.designer.widget import Ui_Widget
from ui.plaintext import PlainText
from ui.theme import Theme
from ui.thread import WidgetThread

__author__ = 'peter'


class MainUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Widget()
        self.ui.setupUi(self)

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
        self.plainTextEdit.setFocus()

        self.plainTextEdit.textChanged.connect(self.onTextChanged)

        self.apps = getAllApps()

        self.center()
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            print("return")
        elif e.key() == Qt.Key_Escape:
            # self.close()
            QCoreApplication.instance().quit()

    def onTextChanged(self):
        print("text changed")
        text = self.plainTextEdit.toPlainText()
        if text:
            t = WidgetThread(self)
            t.finishSignal.connect(self.threadEnd)
            t.start()
        else:
            # clear list
            pass

    def center(self):
        desktop = QApplication.desktop()
        deskRect = desktop.screenGeometry(desktop.screenNumber(QCursor.pos()))
        deskX = deskRect.width()
        deskY = deskRect.height()
        x = deskX / 2 - self.width() / 2 + deskRect.left()
        y = (deskY - Cfg.beginHeight - Cfg.rowSize * (Cfg.maxPrintSize - 1)) * 0.4
        self.move(x, y)

    def threadEnd(self, ls):
        print("thread end")
        for word in ls:
            print(word.name)
            print(word.executable)
            print(word.iconName)
