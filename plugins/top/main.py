# coding=utf-8
import os

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


class Main:
    title = 'Top'
    desc = '显示当前进程'
    keyword = 'top'
    iconName = 'icon.png'

    @staticmethod
    def run(param):
        Main.list(param)
        return False

    @staticmethod
    def list(param):
        if not param or (param[0] != 'c' and param[0] != 'm'):
            return [
                ('Usage', '[c] ordered by %CPU, [m] ordered by %MEM', None),
                ('top c', 'sort by %CPU', None),
                ('top m', 'sort by %MEM', None),
            ]
        if param[0] == 'c':
            f = os.popen('ps axo comm,pid,pcpu,pmem,user,command k -pcpu |head')
        elif param[0] == 'm':
            f = os.popen('ps axo comm,pid,pcpu,pmem,user,command k -pmem |head')
        else:
            return []

        ret = []
        for line in f.readlines()[1:]:
            info = line.split()
            ret.append(
                (info[0],
                 'PID: ' + info[1] + ', CPU: ' + info[2] + '%, RAM: ' + info[3] + '%',
                 getAppIcon(info[5])))
        return ret
