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
        Main.mainCmd = Cmd(title='StackOverflow', desc='在StackOverflow中搜索', icon='icon.png', cmd='so', onRunCmd=Main.run)

    @staticmethod
    def run(param):
        if not param:
            return BasePlugin.setShowCmd('so')
        BasePlugin.openURL("http://stackoverflow.com/search?q=" + "+".join(param.split()))
        return RetVal.close

    @staticmethod
    def onList(param):
        cmd = copy.copy(Main.mainCmd)
        cmd.desc += ' ' + param
        return [cmd]
