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

    def getDesc(self):
        return self.desc

    def set(self, module, path):
        self.name = module.Main.title
        self.desc = module.Main.desc
        self.keyword = module.Main.keyword if hasattr(module.Main, 'keyword') else module.Main.title
        self.plugin = module
        if module.Main.iconName:
            self.iconName = path + '/' + module.Main.iconName
        return self

    def exec(self, cmd):
        return self.plugin.Main.run(cmd.split()[1:])


class BuildInCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.buildIn
        self.desc = None
        self.handler = None

    def getDesc(self):
        return self.desc

    def exec(self, cmd):
        return self.handler(cmd.split()[1:])

    def set(self, name, handler, desc=None, icon=None):
        self.name = name
        self.keyword = name
        self.desc = desc
        self.handler = handler
        if icon:
            self.iconName = Cfg.iconPath + icon
        return self


class BuildInCmdList:
    cmdList = []

    @staticmethod
    def onQuit(params=None):
        SingletonApp.instance.onExit(None, None)
        return True

    @staticmethod
    def init():
        BuildInCmdList.cmdList.clear()
        BuildInCmdList.cmdList.append(BuildInCmd().set('Quit', BuildInCmdList.onQuit, '退出 Linalfred', 'quit.png'))

    @staticmethod
    def getList():
        if not BuildInCmdList.cmdList:
            BuildInCmdList.init()
        return BuildInCmdList.cmdList
