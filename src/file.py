# coding=utf-8
import os

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

__author__ = 'peter'


def isNeedLower(keyword):
    if keyword.islower():
        needLower = True
    else:
        needLower = False
    return needLower


def getFileList(keyword):
    fileName = '*'.join(keyword)
    needLower = isNeedLower(keyword)
    if needLower:
        findCmd = "find " + os.environ['HOME'] + " -iname '*" + fileName + "*' 2>/dev/null"
    else:
        findCmd = "find " + os.environ['HOME'] + " -name '*" + fileName + "*' 2>/dev/null"
    p = os.popen(findCmd)
    return p.readlines()


def getFileIconName(fileName):
    iconTheme = Gtk.IconTheme.get_default()
    file = Gio.File.new_for_path(fileName)
    file_info = file.query_info('standard::icon', Gio.FileQueryInfoFlags.NONE, None)
    icon = Gio.FileInfo.get_icon(file_info)
    iconInfo = Gtk.IconTheme.lookup_by_gicon(iconTheme, icon, 256, Gtk.IconLookupFlags.USE_BUILTIN)
    return iconInfo.get_filename()
