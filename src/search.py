# coding=utf-8
import re

from os.path import basename

from app import App
from cmd import Cmd, CmdType
from config import Cfg
from file import getFileList, getFileIconName

__author__ = 'peter'


class Search:
    @staticmethod
    def getRegex(keyword):
        pattern = '.*?'.join(keyword)
        return re.compile(pattern)

    @staticmethod
    def needLower(keyword):
        if keyword.islower():
            needLower = True
        else:
            needLower = False
        return needLower

    @staticmethod
    def searchApps(keyword, noRegex):
        apps = []
        needLower = Search.needLower(keyword)
        if noRegex:
            for app in App.getAppList():
                if needLower and keyword == app.keyword.lower():
                    apps.append(app)
                elif not needLower and keyword == app.keyword:
                    apps.append(app)
            return apps

        regex = Search.getRegex(keyword)
        for app in App.getAppList():
            match = regex.search(app.keyword.lower() if needLower else app.keyword)
            if match:
                apps.append((len(match.group()), match.start(), app))
        return [x for _, _, x in sorted(apps, key=lambda x: (x[0], x[1], x[2].keyword.lower()))]

    @staticmethod
    def searchFiles(keyword):
        files = []
        needLower = Search.needLower(keyword)
        regex = Search.getRegex(keyword)
        fileList = getFileList(keyword)
        for file in fileList:
            file = file.strip()
            match = regex.search(file.lower() if needLower else file)
            if match:
                files.append((len(match.group()), match.start(), file))
        files = [x for _, _, x in sorted(files)]
        ret = []
        for i in range(min(len(files), Cfg.getInt('ui', 'maxListSize'))):
            f = Cmd()
            f.name = basename(files[i])
            f.keyword = f.name
            f.type = CmdType.file
            f.path = files[i]
            f.iconName = getFileIconName(files[i])
            ret.append(f)
        return ret

    @staticmethod
    def search(keyword):
        if keyword[:1] == ' ':
            # 文件查找
            ret = Search.searchFiles(keyword[1:])
        else:
            # 查找App,插件,内置命令
            ret = Search.searchApps(keyword.split()[0], ' ' in keyword)
        return ret
