# coding=utf-8
from enum import Enum

__author__ = 'peter'


class CmdType(Enum):
    app = 0


class Cmd:
    def __init__(self, type=CmdType.app):
        self.type = type
        # app
        self.name = None
        self.executable = None
        self.iconName = None
        # shortcut
        self.modifier = None
        self.shortcutKey = None

    def __eq__(self, other):
        return self.type == other.type and self.name == other.name and self.executable == self.executable
