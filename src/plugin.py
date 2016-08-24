# coding=utf-8
import os

import sys

from cmd import PluginCmd
from importlib import util

from config import Cfg

__author__ = 'peter'


class Plugin:
    pluginList = []
    sys.path.append(Cfg.pluginPath)

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
                    Plugin.pluginList.append(PluginCmd().set(module, dirFullName))
                except:
                    pass

    @staticmethod
    def getPluginList():
        return sorted(Plugin.pluginList, key=lambda x: x.name.lower())


if __name__ == '__main__':
    Plugin.getAllPlugins()
