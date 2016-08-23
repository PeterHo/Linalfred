# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class Main:
    title = 'ZhiHu'
    desc = '使用知乎搜索'
    keyword = 'zh'
    iconName = 'zhihu.png'

    @staticmethod
    def run(param):
        if not len(param):
            return False
        QProcess.startDetached("xdg-open", ["https://www.zhihu.com/search?type=content&q=" + "+".join(param)])
        return True
