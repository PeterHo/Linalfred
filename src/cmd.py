# coding=utf-8
from enum import Enum

from PyQt5.QtCore import QProcess

from config import Cfg
from singleton import SingletonApp

__author__ = 'peter'


class CmdType(Enum):
    app = 0
    file = 1
    plugin = 2
    buildInCmd = 3


class Cmd:
    def __init__(self, type=CmdType.app):
        self.type = type
        # commons
        self.name = None
        self.keyword = None
        self.iconName = None
        # app
        self.executable = None
        # file
        self.path = None
        # plugin
        self.desc = None
        self.plugin = None
        # build in cmd
        self.handler = None
        # shortcut
        self.modifier = None
        self.shortcutKey = None

    def getDesc(self):
        desc = None
        if self.type == CmdType.app:
            desc = self.executable
        elif self.type == CmdType.file:
            desc = self.path
        elif self.type == CmdType.plugin:
            desc = self.desc
        elif self.type == CmdType.buildInCmd:
            desc = self.desc
        return desc

    def exec(self, cmd):
        if self.type == CmdType.app:
            QProcess.startDetached(self.executable, cmd.split()[1:])
        elif self.type == CmdType.file:
            QProcess.startDetached('xdg-open', [self.path])
        elif self.type == CmdType.plugin:
            return self.plugin.Main.run(cmd.split()[1:])
        elif self.type == CmdType.buildInCmd:
            return self.handler(cmd.split()[1:])
        return True

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name and self.executable == self.executable


class BuildInCmd:
    cmdList = []

    @staticmethod
    def initOneCmd(name, handler, desc=None, icon=None):
        cmd = Cmd()
        cmd.name = name
        cmd.keyword = name
        cmd.type = CmdType.buildInCmd
        cmd.desc = desc
        cmd.handler = handler
        if icon:
            cmd.iconName = Cfg.iconPath + icon
        return cmd

    @staticmethod
    def initBuildInCmdList():
        BuildInCmd.cmdList.clear()
        BuildInCmd.cmdList.append(BuildInCmd.initOneCmd('Quit', BuildInCmd.onQuit, '退出 Linalfred', 'quit.png'))

    @staticmethod
    def onQuit(params=None):
        SingletonApp.instance.onExit(None, None)
        return True

    @staticmethod
    def getBuildInCmdList():
        if not BuildInCmd.cmdList:
            BuildInCmd.initBuildInCmdList()
        return BuildInCmd.cmdList
