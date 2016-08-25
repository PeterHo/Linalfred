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
        Main.mainCmd = Cmd(title='GitHub', desc='使用GitHub搜索', icon='github.png', cmd='gh', onRunCmd=Main.run)

    @staticmethod
    def run(param):
        if not param:
            return BasePlugin.setShowCmd('gh')
        BasePlugin.openURL("https://github.com/search?q=" + "+".join(param.split()))
        return RetVal.close

    @staticmethod
    def onList(param):
        cmd = copy.copy(Main.mainCmd)
        cmd.desc += ' ' + param
        return [cmd]
