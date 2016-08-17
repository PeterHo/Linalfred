#!/usr/bin/python3
# coding=utf-8
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.maindlg import MainDlg

__author__ = 'peter'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = MainDlg()
    sys.exit(app.exec_())
