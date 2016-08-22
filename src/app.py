# coding=utf-8
from functools import reduce

from cmd import Cmd, CmdType, BuildInCmd

import gi

from plugin import Plugin

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

__author__ = 'peter'


class App:
    apps = []

    @staticmethod
    def getAllApps():
        App.apps.clear()
        iconTheme = Gtk.IconTheme.get_default()
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
            appInfo.keyword = name.replace(' ', '')
            appInfo.executable = executable
            appInfo.iconName = iconName
            App.apps.append(appInfo)

        # 去重
        App.apps = reduce(lambda x, y: x if y in x else x + [y], [[], ] + App.apps)
        # 加入脚本命令
        App.apps += Plugin.getPluginList()
        # 加入内置命令
        App.apps += BuildInCmd.getBuildInCmdList()
        App.apps.sort(key=lambda x: x.name.lower())
        return App.apps

    @staticmethod
    def getAppList():
        return App.apps
