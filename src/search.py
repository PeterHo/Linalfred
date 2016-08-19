# coding=utf-8
import os
import re

from PyQt5.QtCore import QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileIconProvider
from os.path import basename

from cmd import Cmd, CmdType

import gi

from config import Cfg
from file import getFileList, getFileIconName

gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

__author__ = 'peter'


class Search:
    def getRegex(self, keyword):
        pattern = '.*?'.join(keyword)
        return re.compile(pattern)

    def needLower(self, keyword):
        if keyword.islower():
            needLower = True
        else:
            needLower = False
        return needLower

    def searchApps(self, keyword, allApps):
        apps = []
        needLower = self.needLower(keyword)
        regex = self.getRegex(keyword)
        for app in allApps:
            match = regex.search(app.name.lower() if needLower else app.name)
            if match:
                apps.append((len(match.group()), match.start(), app))
        return [x for _, _, x in sorted(apps, key=lambda x: (x[0], x[1], x[2].name.lower()))]

    def searchFiles(self, keyword):
        files = []
        needLower = self.needLower(keyword)
        regex = self.getRegex(keyword)
        fileList = getFileList(keyword)
        for file in fileList:
            file = file.strip()
            match = regex.search(file.lower() if needLower else file)
            if match:
                files.append((len(match.group()), match.start(), file))
        files = [x for _, _, x in sorted(files)]
        ret = []
        for i in range(min(len(files), Cfg.UI.maxListSize)):
            f = Cmd()
            f.name = basename(files[i])
            f.type = CmdType.file
            f.executable = files[i]
            f.iconName = getFileIconName(files[i])
            ret.append(f)
        return ret
