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
        cmd = self.widget.plainTextEdit.toPlainText()
        search = Search()
        ret = search.searchApps(cmd, self.widget.apps)
        self.widget.mutexThread.lock()
        if cmd == self.widget.plainTextEdit.toPlainText():
            self.finishSignal.emit(ret)
        self.widget.mutexThread.unlock()

