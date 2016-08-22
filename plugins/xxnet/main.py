# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class Main:
    title = 'XX-Net'
    desc = '开启XX-net'
    keyword = 'xx-net'
    iconName = 'favicon.ico'

    @staticmethod
    def run(param=None):
        QProcess.startDetached("/bin/bash", ["/home/peter/Downloads/XX-Net-3.1.19/start"])
        return True
