# coding=utf-8
import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

__author__ = 'peter'


# 通过快捷键切换窗口的小工具
class WndInfo:
    def __init__(self, wid=None, desktop=None, pid=None, user=None, title=None):
        self.wid = wid
        self.desktop = desktop
        self.pid = pid
        self.user = user
        self.title = title


class ProcessInfo:
    def __init__(self, pid=None, user=None, command=None):
        self.pid = pid
        self.user = user
        self.command = command

    @staticmethod
    def getByPid(processList, pid):
        for process in processList:
            if process.pid == pid:
                return process
        return None


# 获得所有窗口
def getWndList():
    wndList = []
    f = os.popen('wmctrl -lp')
    for line in f.readlines():
        info = line.split()
        wndList.append(WndInfo(info[0], info[1], info[2], info[3], ' '.join(info[4:])))
    return sorted(wndList, key=lambda x: x.wid)


# 获得所有进程
def getProcessList():
    processList = []
    f = os.popen('ps axo pid,user,command')
    for line in f.readlines()[1:]:
        info = line.split()
        processList.append(ProcessInfo(info[0], info[1], info[2]))
    return processList


hotKeys = [
    ('<Mod4>Q', '/usr/lib/firefox/firefox'),
    ('<Mod4>W', 'nemo'),
    ('<Mod4>E', '/usr/lib/gnome-terminal/gnome-terminal-server'),
    ('<Mod4>A', '/home/peter/tools/android-studio/bin/../jre/bin/java'),
    ('<Mod4>S', '/home/peter/tools/pycharm/bin/../jre/jre/bin/java'),
    ('<Mod4>F', '/home/peter/tools/clion/bin/../jre/jre/bin/java'),
    ('<Mod4>Z', 'okular'),
    ('<Mod4>X', '/home/peter/src/WizNote/WizNote'),
]

lastWid = None


def switchToNextWnd(wndList):
    global lastWid
    if len(wndList) == 1 or lastWid is None or lastWid not in wndList:
        # 只有一个窗口,或上次记录不在列表中,或不存在上次记录,直接切换
        lastWid = wndList[0]
        os.popen('wmctrl -ia ' + wndList[0])
    else:
        # 依次切换
        for idx, wnd in enumerate(wndList):
            if wnd == lastWid:
                lastWid = wndList[(idx + 1) % len(wndList)]
                os.popen('wmctrl -ia ' + lastWid)
                return


def switchToWnd(cmd):
    wndList = getWndList()
    processList = getProcessList()
    canSwitchList = []
    # 获得可以切换的窗口
    for wnd in wndList:
        if wnd.desktop != '-1':
            process = ProcessInfo.getByPid(processList, wnd.pid)
            if process and process.command == cmd:
                canSwitchList.append(wnd.wid)
    if canSwitchList:
        switchToNextWnd(canSwitchList)
    else:
        os.popen(cmd)


def onSwitchWnd(hotkey):
    for key in hotKeys:
        keyVal, modifiers = Gtk.accelerator_parse(key[0])
        if keyVal == hotkey.keyVal and modifiers == hotkey.modifiers:
            switchToWnd(key[1])
            return True
    return False


def addSwitchWndHotKeys(key):
    for hotkey in hotKeys:
        key.grab(hotkey[0])
