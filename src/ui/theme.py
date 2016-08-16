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
            self.beginHeight = 125
            self.listWidgetY = 91
            self.dimensions = QSize(550, 75)
            self.groupBoxStylesheet = "QGroupBox{background:white;border-radius: 9px;}"
            self.plainTextEditStylesheet = "QPlainTextEdit{border: 1px solid white}"
            self.listWidgetStylesheet = "QListWidget{border: 1px solid white} QListWidget::item{padding : 3px 3px 3px 3px}"
            self.fontSize = 40
            self.blurRadius = 9.0
            self.shadowColor = QColor(0, 0, 0, 160)
            self.shadowOffset = 3.0
        elif themeName == "Dark":
            self.beginHeight = 94
            self.listWidgetY = 65
            self.dimensions = QSize(550, 50)
            self.groupBoxStylesheet = "QGroupBox{background:#444444;border-radius: 9px; padding: -3px -3px -3px -3px;}"
            self.plainTextEditStylesheet = "QPlainTextEdit{background:#3a3a3a; border: 1px solid #3a3a3a; color: #AAAAAA}"
            self.listWidgetStylesheet = """
                QListWidget { background: #444444; border: 1px solid #444444}
                QListWidget::item { background: #444444; padding: 0px 0px 0px 3px;}
                QListWidget::item:selected { background: #525252; border: 1px solid #AAAAAA; border-radius: 2px;}
                QLabel {color: #AAAAAA;}
                """
            self.fontSize = 30
            self.blurRadius = 10.0
            self.shadowColor = QColor(0, 0, 0, 200)
            self.shadowOffset = 0.0
