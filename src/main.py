#!/usr/bin/python3
# coding=utf-8
import sys

from singleton import SingletonApp
from switchwnd import initSwitchWnd
from ui.maindlg import MainDlg

__author__ = 'peter'

if __name__ == "__main__":
    initSwitchWnd()
    app = SingletonApp(sys.argv)
    if app.is_running:
        app.send_message(sys.argv)
    else:
        dlg = MainDlg()
        dlg.show()
        app.setDlg(dlg)
        sys.exit(app.exec_())
