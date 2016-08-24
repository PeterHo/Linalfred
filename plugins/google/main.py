# coding=utf-8
from plugin_common.Plugin import Plugin

__author__ = 'peter'


class Main(Plugin):
    title = 'Google'
    desc = '使用谷歌搜索'
    keyword = 'g'
    iconName = 'google.png'

    @staticmethod
    def run(param):
        if not param:
            return False
        Plugin.openURL("https://www.google.com/search?q=" + "+".join(param))
        return True

    @staticmethod
    def list(param):
        return [(None, Main.desc + " " + " ".join(param), None, None)]
