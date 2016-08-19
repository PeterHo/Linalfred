# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class Main:
    title = 'BaiDu'
    desc = '使用百度搜索'
    iconName = 'baidu.png'

    @staticmethod
    def run(param):
        if not len(param):
            return False
        QProcess.startDetached("xdg-open", ["http://www.baidu.com/s?wd=" + "+".join(param)])
        return True
