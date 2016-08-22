# coding=utf-8
from functools import reduce

from cmd import AppCmd, BuildInCmdList

import gi

from plugin import Plugin

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

__author__ = 'peter'


class AppList:
    apps = []

    @staticmethod
    def getAllApps():
        AppList.apps.clear()
        iconTheme = Gtk.IconTheme.get_default()
        appList = Gio.AppInfo.get_all()
        for app in appList:
            name = Gio.AppInfo.get_display_name(app)
            executable = Gio.AppInfo.get_executable(app)
            iconName = None
            icon = Gio.AppInfo.get_icon(app)
            if icon:
                iconInfo = Gtk.IconTheme.lookup_by_gicon(iconTheme, icon, 256, Gtk.IconLookupFlags.USE_BUILTIN)
                if iconInfo:
                    iconName = iconInfo.get_filename()

            AppList.apps.append(AppCmd().set(name=name, executable=executable, iconName=iconName))

        # 去重
        AppList.apps = reduce(lambda x, y: x if y in x else x + [y], [[], ] + AppList.apps)
        # 加入脚本命令
        AppList.apps += Plugin.getPluginList()
        # 加入内置命令
        AppList.apps += BuildInCmdList.getList()
        AppList.apps.sort(key=lambda x: x.name.lower())
        return AppList.apps

    @staticmethod
    def getAppList():
        return AppList.apps
