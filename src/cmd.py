# coding=utf-8
from enum import Enum

from PyQt5.QtCore import QProcess

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
        self.iconName = None
        # app
        self.executable = None
        # file
        self.path = None
        # plugin
        self.desc = None
        self.plugin = None
        # build in cmd

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
        return desc

    def exec(self, cmd):
        if self.type == CmdType.app:
            QProcess.startDetached(self.executable)
        elif self.type == CmdType.file:
            QProcess.startDetached('xdg-open', [self.path])
        elif self.type == CmdType.plugin:
            return self.plugin.Main.run(cmd.split()[1:])
        return True

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name and self.executable == self.executable


def getBuildInCmdList():
    return []
