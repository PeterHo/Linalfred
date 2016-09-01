# coding=utf-8
from enum import Enum

import sys
from PyQt5.QtCore import QProcess

from config import Cfg

sys.path.append(Cfg.pluginPath)
from plugin_common.baseplugin import RetVal
from singleton import SingletonApp

__author__ = 'peter'


class CmdType(Enum):
    app = 0
    file = 1
    plugin = 2
    buildIn = 3
    fileManager = 4


class Cmd:
    def __init__(self):
        self.type = None
        # commons
        self.name = None
        self.keyword = None
        self.iconName = None
        # shortcut
        self.modifier = None
        self.shortcutKey = None

    def getDesc(self):
        pass

    def list(self, cmd):
        return [self]

    def exec(self, cmd):
        pass

    def complement(self, cmd):
        if len(cmd) <= len(self.keyword):
            return self.keyword + " "
        else:
            return cmd

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name


class AppCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.app
        self.executable = None

    def getDesc(self):
        return self.executable

    def exec(self, cmd):
        # 执行程序,命令截掉keyword以后就是参数
        QProcess.startDetached(self.executable, cmd[len(self.keyword):].split())
        return RetVal.close

    def set(self, name=None, keyword=None, executable=None, iconName=None):
        self.name = name
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = name
        self.executable = executable
        self.iconName = iconName
        return self

    def __eq__(self, other):
        return super().__eq__(other) and self.executable == self.executable


class FileCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.file
        self.path = None

    def getDesc(self):
        return self.path

    def exec(self, cmd):
        QProcess.startDetached('xdg-open', [self.path])
        return RetVal.close

    def set(self, name=None, keyword=None, path=None, iconName=None):
        self.name = name
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = self.name
        self.path = path
        self.iconName = iconName
        return self

    def complement(self, cmd):
        return cmd


class PluginCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.plugin
        self.desc = None
        self.plugin = None
        self.pluginParam = None
        self.path = None
        self.onRunCmd = None

    def copy(self):
        new = PluginCmd()
        new.plugin = self.plugin
        new.path = self.path
        return new

    def getDesc(self):
        return self.desc

    def setIconName(self, iconName):
        if iconName:
            if '/' in iconName:
                self.iconName = iconName
            else:
                self.iconName = self.path + '/' + iconName

    def setByPluginCmd(self, cmd):
        self.name = cmd.title
        self.desc = cmd.desc
        self.keyword = cmd.cmd
        self.pluginParam = cmd.param
        self.setIconName(cmd.icon)
        self.onRunCmd = cmd.onRunCmd

    def set(self, module, path):
        self.plugin = module
        self.path = path
        self.setByPluginCmd(module.mainCmd)
        return self

    def list(self, cmd):
        showList = []
        cmdList = self.plugin.onList(cmd[len(self.keyword):].strip())
        if not cmdList:
            return [self]
        for cmd in cmdList:
            subCmd = self.copy()
            subCmd.setByPluginCmd(cmd)
            showList.append(subCmd)
        return showList

    def exec(self, cmd):
        if self.pluginParam:
            return self.onRunCmd(self.pluginParam)
        return self.onRunCmd(cmd[len(self.keyword):].strip())


class BuildInCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.buildIn
        self.desc = None
        self.handler = None
        self.listFun = None

    def getDesc(self):
        return self.desc

    def list(self, cmd):
        if self.listFun:
            return self.listFun(cmd.split()[1:])
        return [self]

    def exec(self, cmd):
        return self.handler(cmd.split()[1:])

    def set(self, name, handler, desc=None, icon=None, listFun=None):
        self.name = name
        self.keyword = name
        self.desc = desc
        self.handler = handler
        if icon:
            self.iconName = Cfg.iconPath + icon
        self.listFun = listFun
        return self


class BuildInCmdList:
    cmdList = []

    @staticmethod
    def onQuitExec(params=None):
        SingletonApp.instance.onExit(None, None)
        return RetVal.close

    @staticmethod
    def onRefreshAppExec(params=None):
        from app import AppList
        AppList.getAllApps()
        print("refresh app")
        return RetVal.close

    @staticmethod
    def init():
        BuildInCmdList.cmdList.clear()
        BuildInCmdList.cmdList.append(
            BuildInCmd().set('Quit', BuildInCmdList.onQuitExec, '退出 Linalfred', 'quit.png'))
        BuildInCmdList.cmdList.append(
            BuildInCmd().set('RefreshApp', BuildInCmdList.onRefreshAppExec, '刷新已安装应用', 'refresh.jpg'))
        BuildInCmdList.cmdList.sort(key=lambda x: x.name.lower())

    @staticmethod
    def getList():
        if not BuildInCmdList.cmdList:
            BuildInCmdList.init()
        return BuildInCmdList.cmdList
