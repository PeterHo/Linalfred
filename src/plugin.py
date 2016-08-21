# coding=utf-8
import os
from cmd import Cmd, CmdType
from importlib import util

from config import Cfg

__author__ = 'peter'


class Plugin:
    pluginList = []

    @staticmethod
    def getAllPlugins():
        Plugin.pluginList.clear()
        dirList = os.listdir(Cfg.pluginPath)
        for dir in dirList:
            dirFullName = Cfg.pluginPath + dir
            pluginFullName = dirFullName + '/main.py'
            if os.path.isdir(dirFullName) and os.path.exists(pluginFullName):
                try:
                    spec = util.spec_from_file_location('main', pluginFullName)
                    module = util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    cmd = Cmd()
                    cmd.type = CmdType.plugin
                    cmd.name = module.Main.title
                    cmd.desc = module.Main.desc
                    cmd.keyword = module.Main.keyword if hasattr(module.Main, 'keyword') else module.Main.title
                    cmd.plugin = module
                    if module.Main.iconName:
                        cmd.iconName = dirFullName + '/' + module.Main.iconName
                    Plugin.pluginList.append(cmd)
                except:
                    pass

    @staticmethod
    def getPluginList():
        return Plugin.pluginList


if __name__ == '__main__':
    Plugin.getAllPlugins()
