# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class Plugin:
    @staticmethod
    def openURL(url):
        QProcess.startDetached("xdg-open", [url])
