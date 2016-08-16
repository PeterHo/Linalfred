#!/usr/bin/python3
# coding=utf-8

from PyQt5.QtCore import *
from PyQt5.QtGui import *

__author__ = 'peter'


class Theme(object):
    def __init__(self, themeName):
        self.beginHeight = 0
        self.listWidgetY = 0
        self.dimensions = QSize()
        self.groupBoxStylesheet = ""
        self.plainTextEditStylesheet = ""
        self.listWidgetStylesheet = ""
        self.fontSize = 0
        self.blurRadius = 0.0
        self.shadowColor = QColor()
        self.shadowOffset = 0.0

        if themeName == "Classic":
            self.globalBeginHeight = 125
            self.globalListWidgetY = 91
            self.dimensions = QSize(550, 75)
            self.groupBoxStylesheet = "QGroupBox{background:white;border-radius: 9px;}"
            self.plainTextEditStylesheet = "QPlainTextEdit{border: 1px solid white}"
            self.listWidgetStylesheet = "QListWidget{border: 1px solid white} QListWidget::item{padding : 3px 3px 3px 3px}"
            self.fontSize = 40
            self.blurRadius = 9.0
            self.shadowColor = QColor(0, 0, 0, 160)
            self.shadowOffset = 3.0
