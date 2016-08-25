# coding=utf-8
import os

from plugin_common.baseplugin import BasePlugin
from plugin_common.baseplugin import Cmd

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

__author__ = 'peter'

appList = []


def getAppIcon(name):
    global appList
    iconTheme = Gtk.IconTheme.get_default()
    if not appList:
        appList = Gio.AppInfo.get_all()
    for app in appList:
        if name == Gio.AppInfo.get_display_name(app) or \
                        name == Gio.AppInfo.get_executable(app) or \
                        os.path.basename(name) == Gio.AppInfo.get_display_name(app) or \
                        os.path.basename(name) == os.path.basename(Gio.AppInfo.get_executable(app)):
            icon = Gio.AppInfo.get_icon(app)
            if icon:
                iconInfo = Gtk.IconTheme.lookup_by_gicon(iconTheme, icon, 256, Gtk.IconLookupFlags.USE_BUILTIN)
                if iconInfo:
                    return iconInfo.get_filename()
    return 'app.png'


class Main(BasePlugin):
    mainCmd = None
    subCmdList = []

    @staticmethod
    def init():
        Main.mainCmd = Cmd(title='Top', desc='显示当前进程', icon='icon.png', cmd='top')

        Main.subCmdList = [
            Cmd(title='top c', desc='sort by %CPU', icon=Main.mainCmd.icon, cmd='top c'),
            Cmd(title='top m', desc='sort by %MEM', icon=Main.mainCmd.icon, cmd='top m'),
        ]

    @staticmethod
    def onList(param):
        if not param:
            return Main.subCmdList
        if param[0] == 'c':
            f = os.popen('ps axo comm,pid,pcpu,pmem,user,command k -pcpu |head')
        elif param[0] == 'm':
            f = os.popen('ps axo comm,pid,pcpu,pmem,user,command k -pmem |head')
        else:
            return []

        topList = []
        for line in f.readlines()[1:]:
            info = line.split()
            topList.append(
                Cmd(title=info[0], desc='PID: ' + info[1] + ', CPU: ' + info[2] + '%, RAM: ' + info[3] + '%',
                    icon=getAppIcon(info[5]), cmd='top ' + param[0]))
        return topList
