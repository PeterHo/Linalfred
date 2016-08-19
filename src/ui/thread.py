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
        search = Search()
        if cmd[:1] == ' ':
            # 文件查找
            ret = search.searchFiles(cmd[1:])
        else:
            ret = search.searchApps(cmd, self.dlg.apps)
        self.dlg.mutexThread.lock()
        if cmd == self.dlg.editBox.toPlainText():
            self.finishSignal.emit(ret)
        self.dlg.mutexThread.unlock()

