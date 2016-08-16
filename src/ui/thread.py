# coding=utf-8
import time
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

__author__ = 'peter'


class WidgetThread(QThread):
    finishSignal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = parent

    def run(self):
        cmd = self.widget.plainTextEdit.toPlainText()
        print(cmd)
        time.sleep(2)
        self.finishSignal.emit(['hello,', 'world', '!'])
