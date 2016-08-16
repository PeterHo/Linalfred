# coding=utf-8
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget

from ui.config import Cfg
from ui.designer.listitem import Ui_ListItem

__author__ = 'peter'


class ListItem(QWidget):
    def __init__(self, icon, text, cmd, parent=None):
        super().__init__(parent)
        self.ui = Ui_ListItem()
        self.ui.setupUi(self)

        self.ui.cmd.setStyleSheet("QLabel{color: rgb(100, 100, 100)}")
        fm = QFontMetrics(self.ui.text.font())
        self.ui.text.setText(fm.elidedText(text, Qt.ElideRight, self.ui.text.width()))
        self.ui.cmd.setText(cmd)
        if icon:
            qIcon = QIcon(icon)
        else:
            qIcon = QIcon(Cfg.defaultIcon)
        p = qIcon.pixmap(QSize(Cfg.iconSize, Cfg.iconSize))
        self.ui.icon.setPixmap(p)
