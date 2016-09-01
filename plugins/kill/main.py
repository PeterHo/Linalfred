# coding=utf-8
import os
import re

from plugin_common.baseplugin import BasePlugin, RetVal
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
        Main.mainCmd = Cmd(title='kill', desc='杀死指定进程', icon='kill.png', cmd='kill')

    @staticmethod
    def getRegex(keyword):
        pattern = '.*?'.join(keyword)
        return re.compile(pattern)

    @staticmethod
    def onList(param):
        if not param:
            return [Main.mainCmd]
        f = os.popen('ps axo comm,pid,command')

        killList = []
        regex = Main.getRegex(param)
        for line in f.readlines()[1:]:
            info = line.split()
            match = regex.search(info[0].lower())
            if match:
                killList.append((len(match.group()), match.start(), info))
        infos = [x for _, _, x in sorted(killList, key=lambda x: (x[0], x[1], x[2][0].lower()))]

        killList.clear()
        for info in infos:
            killList.append(
                Cmd(title=info[0], desc=info[1] + ' ' + info[2],
                    icon=getAppIcon(info[2]), cmd='kill', param=info[1], onRunCmd=Main.onKill))
        return killList

    @staticmethod
    def onKill(param):
        if not param:
            return [Main.mainCmd]
        print(param)
        BasePlugin.execute(["kill", "-9", param])
        return RetVal.close
