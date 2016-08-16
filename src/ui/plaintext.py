# coding=utf-8
from PyQt5.QtWidgets import QPlainTextEdit

__author__ = 'peter'


class PlainText(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.listWidget = None
