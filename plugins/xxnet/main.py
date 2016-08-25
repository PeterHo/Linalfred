# coding=utf-8
from plugin_common.baseplugin import BasePlugin, RetVal
from plugin_common.baseplugin import Cmd

__author__ = 'peter'


class Main(BasePlugin):
    mainCmd = None
    subCmdList = []

    @staticmethod
    def init():
        Main.mainCmd = Cmd(title='XX-Net', desc='开启XX-net', icon='favicon.ico', cmd='xx-net', onRunCmd=Main.run)

    @staticmethod
    def run(param):
        BasePlugin.bash(["/home/peter/Downloads/XX-Net-3.1.19/start"])
        return RetVal.close
