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
        Main.mainCmd = Cmd(title='Google', desc='使用谷歌搜索', icon='google.png', cmd='g', onRunCmd=Main.run)

    @staticmethod
    def run(param):
        if not param:
            return BasePlugin.setShowCmd('g')
        # BasePlugin.openURL("https://www.google.com/search?q=" + "+".join(param.split()))
        BasePlugin.openURL("https://www.google.com.hk/?gws_rd=cr,ssl#newwindow=1&safe=strict&q=" + "+".join(param.split()))
        return RetVal.close

    @staticmethod
    def onList(param):
        cmd = copy.copy(Main.mainCmd)
        cmd.desc += ' ' + param
        return [cmd]
