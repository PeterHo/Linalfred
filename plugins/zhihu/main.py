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
        Main.mainCmd = Cmd(title='ZhiHu', desc='使用知乎搜索', icon='zhihu.png', cmd='zh', onRunCmd=Main.run)

    @staticmethod
    def run(param):
        if not param:
            return BasePlugin.setShowCmd('g')
        BasePlugin.openURL("https://www.zhihu.com/search?type=content&q=" + "+".join(param.split()))
        return RetVal.close

    @staticmethod
    def onList(param):
        cmd = copy.copy(Main.mainCmd)
        cmd.desc += ' ' + param
        return [cmd]
