# coding=utf-8
from cmd import Cmd, CmdType

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

__author__ = 'peter'


def getAllApps():
    iconTheme = Gtk.IconTheme.get_default()
    apps = []
    appList = Gio.AppInfo.get_all()
    for app in appList:
        appInfo = Cmd(CmdType.app)
        name = Gio.AppInfo.get_display_name(app)
        executable = Gio.AppInfo.get_executable(app)
        iconName = None
        icon = Gio.AppInfo.get_icon(app)
        if icon:
            iconInfo = Gtk.IconTheme.lookup_by_gicon(iconTheme, icon, 256, Gtk.IconLookupFlags.USE_BUILTIN)
            if iconInfo:
                iconName = iconInfo.get_filename()

        appInfo.name = name
        appInfo.executable = executable
        appInfo.iconName = iconName
        apps.append(appInfo)

    apps.sort(key=lambda x: x.name.lower())
    return apps
