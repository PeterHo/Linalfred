#!/usr/bin/python3
# coding=utf-8

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from config import Cfg

__author__ = 'peter'


class Theme(object):
    def __init__(self, themeName=None):
        # main dialog
        self.dlgHeight = 125
        self.blurRadius = 9.0
        self.shadowColor = QColor(0, 0, 0, 160)
        self.shadowOffset = 3.0

        # 输入框
        self.editBoxSize = QSize(550, 75)
        self.editBoxFontSize = 40
        self.editBoxStylesheet = "QPlainTextEdit{background:#EEEEEC; border: 1px solid white}"

        # 列表项
        self.rowSize = 51
        self.iconSize = 42
        self.listFontSize = 20
        self.defaultIcon = 'application-x-executable.png'

        # 列表
        self.listY = 91
        self.listStylesheet = "QListWidget{border: 1px solid white} QListWidget::item{padding : 3px 3px 3px 3px}"
        self.groupBoxStylesheet = "QGroupBox{background:white;border-radius: 9px;}"

        if themeName == "Classic":
            self.dlgHeight = 94
            self.blurRadius = 10.0
            self.shadowOffset = 0.0

            self.editBoxSize = QSize(550, 50)
            self.editBoxFontSize = 28

            self.listY = 65
            self.listStylesheet = """
                QListWidget{border: 1px solid white} QListWidget::item{padding : 0px 0px 0px 3px}
                """
            self.groupBoxStylesheet = "QGroupBox{background:white;border-radius: 9px; padding: -3px -3px -3px -3px;}"
        elif themeName == "Dark":
            self.dlgHeight = 94
            self.blurRadius = 10.0
            self.shadowColor = QColor(0, 0, 0, 200)
            self.shadowOffset = 0.0

            self.editBoxSize = QSize(550, 50)
            self.editBoxFontSize = 30
            self.editBoxStylesheet = "QPlainTextEdit{background:#3a3a3a; border: 1px solid #3a3a3a; color: #AAAAAA}"

            self.listY = 65
            self.listStylesheet = """
                QListWidget { background: #444444; border: 1px solid #444444}
                QListWidget::item { background: #444444; padding: 0px 0px 0px 3px;}
                QListWidget::item:selected { background: #525252; border: 1px solid #AAAAAA; border-radius: 2px;}
                QLabel {color: #AAAAAA;}
                """
            self.groupBoxStylesheet = "QGroupBox{background:#444444;border-radius: 9px; padding: -3px -3px -3px -3px;}"

    def getDefaultIcon(self, type):
        return Cfg.iconPath + self.defaultIcon
