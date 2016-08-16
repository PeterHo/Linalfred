# coding=utf-8
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from search import Search

__author__ = 'peter'


class WidgetThread(QThread):
    finishSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = parent

    def run(self):
        text = self.widget.plainTextEdit.toPlainText()
        search = Search()
        ret = search.searchApps(text, self.widget.apps)
        self.finishSignal.emit(ret)
