#!/usr/bin/python3
# coding=utf-8
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

__author__ = 'peter'


class Dlg(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/test.ui', self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = Dlg()
    dlg.show()
    sys.exit(app.exec_())
