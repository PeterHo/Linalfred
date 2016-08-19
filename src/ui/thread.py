# coding=utf-8
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

from search import Search

__author__ = 'peter'


class DlgThread(QThread):
    finishSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dlg = parent

    def run(self):
        cmd = self.dlg.editBox.toPlainText()
        if cmd:
            ret = Search.search(cmd)
            self.dlg.mutexThread.lock()
            if cmd == self.dlg.editBox.toPlainText():
                self.finishSignal.emit(ret)
            self.dlg.mutexThread.unlock()
