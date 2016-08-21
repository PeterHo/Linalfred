# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class Main:
    title = 'GitHub'
    desc = '使用GitHub搜索'
    keyword = 'gh'
    iconName = 'github.png'

    @staticmethod
    def run(param):
        if not len(param):
            return False
        QProcess.startDetached("xdg-open", ["https://github.com/search?q=" + "+".join(param)])
        return True
