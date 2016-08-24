# coding=utf-8
from abc import abstractmethod
from enum import Enum

from PyQt5.QtCore import QProcess

from config import Cfg
from singleton import SingletonApp

__author__ = 'peter'


class CmdType(Enum):
    app = 0
    file = 1
    plugin = 2
    buildIn = 3


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

    @abstractmethod
    def getDesc(self):
        pass

    @abstractmethod
    def exec(self, cmd):
        pass

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
        QProcess.startDetached(self.executable, cmd.split()[1:])
        return True

    def set(self, name=None, keyword=None, executable=None, iconName=None):
        self.name = name
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = name.replace(' ', '')
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
        return True

    def set(self, name=None, keyword=None, path=None, iconName=None):
        self.name = name
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = self.name
        self.path = path
        self.iconName = iconName
        return self


class PluginCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.plugin
        self.desc = None
        self.plugin = None
        self.path = None

    def copy(self):
        new = PluginCmd()
        new.type = self.type
        new.desc = self.desc
        new.plugin = self.plugin
        new.name = self.name
        new.keyword = self.keyword
        new.iconName = self.iconName
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

    def set(self, module, path):
        self.name = module.Main.title
        self.desc = module.Main.desc
        self.keyword = module.Main.keyword if hasattr(module.Main, 'keyword') else module.Main.title
        self.plugin = module
        self.path = path
        self.setIconName(module.Main.iconName)
        return self

    def list(self, cmd):
        if hasattr(self.plugin.Main, 'list'):
            showList = []
            list_ = self.plugin.Main.list(cmd.split()[1:])
            for l in list_:
                new = self.copy()
                if l[0]:
                    new.name = l[0]
                if l[1]:
                    new.desc = l[1]
                if l[2]:
                    new.setIconName(l[2])
                showList.append(new)
            return showList

        return [self]

    def exec(self, cmd):
        return self.plugin.Main.run(cmd.split()[1:])


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
        return True

    @staticmethod
    def onRefreshAppExec(params=None):
        from app import AppList
        AppList.getAllApps()
        print("refresh app")
        return True

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
