# coding=utf-8
from PyQt5.QtCore import QProcess

__author__ = 'peter'


class RetVal:
    keep = "keep"
    close = "close"
    cmd = "cmd:"


class Cmd:
    def __init__(self, title='CmdTitle', desc='CmdDesc', icon=None, cmd=None, param=None, onRunCmd=None):
        # 命令标题, 用于在列表中显示
        self.title = title
        # 命令描述, 用于在列表中显示
        self.desc = desc
        # 命令图标, 用于在列表中显示
        self.icon = icon
        # 具体命令
        self.cmd = cmd
        # 命令参数
        self.param = param
        # 执行命令时的处理方法
        if onRunCmd:
            self.onRunCmd = onRunCmd
        else:
            self.onRunCmd = lambda x: BasePlugin.setShowCmd(self.cmd)


class BasePlugin:
    @staticmethod
    def setShowCmd(cmd):
        return RetVal.cmd + cmd + " "

    @staticmethod
    def listMyself(param):
        return []

    @staticmethod
    def openURL(url):
        QProcess.startDetached("xdg-open", [url])

    @staticmethod
    def bash(param):
        QProcess.startDetached("/bin/bash", param)
