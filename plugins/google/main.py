# coding=utf-8
from plugin_common.baseplugin import BasePlugin

__author__ = 'peter'


class Main(BasePlugin):
    title = 'Google'
    desc = '使用谷歌搜索'
    keyword = 'g'
    iconName = 'google.png'

    @staticmethod
    def run(param):
        if not param:
            return BasePlugin.keep
        BasePlugin.openURL("https://www.google.com/search?q=" + "+".join(param))
        return BasePlugin.close

    @staticmethod
    def list(param):
        return [(None, Main.desc + " " + " ".join(param), None, None)]
