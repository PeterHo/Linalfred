# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class Main:
    title = 'Google'
    desc = '使用谷歌搜索'
    keyword = 'g'
    iconName = 'google.png'

    @staticmethod
    def run(param):
        if not len(param):
            return False
        QProcess.startDetached("xdg-open", ["https://www.google.com/search?q=" + "+".join(param)])
        return True
