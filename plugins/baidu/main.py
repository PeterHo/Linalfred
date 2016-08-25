# coding=utf-8
import copy

from plugin_common.baseplugin import BasePlugin, RetVal
from plugin_common.baseplugin import Cmd

__author__ = 'peter'


class Main(BasePlugin):
    mainCmd = None
    subCmdList = []

    @staticmethod
    def init():
        Main.mainCmd = Cmd(title='BaiDu', desc='使用百度搜索', icon='baidu.png', cmd='b', onRunCmd=Main.run)

    @staticmethod
    def run(param):
        if not param:
            return BasePlugin.setShowCmd('b')
        BasePlugin.openURL("http://www.baidu.com/s?wd=" + "+".join(param.split()))
        return RetVal.close

    @staticmethod
    def onList(param):
        cmd = copy.copy(Main.mainCmd)
        cmd.desc += ' ' + param
        return [cmd]
