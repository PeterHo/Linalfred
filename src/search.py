# coding=utf-8
import re

from os.path import basename

from app import AppList
from cmd import FileCmd
from common import isNeedLower
from config import Cfg
from file import getFileList, getFileIconName

__author__ = 'peter'


class Search:
    @staticmethod
    def getRegex(keyword):
        pattern = '.*?'.join(keyword)
        return re.compile(pattern)

    @staticmethod
    def searchApps(keyword, noRegex):
        apps = []
        needLower = isNeedLower(keyword)
        if noRegex:
            for app in AppList.getAppList():
                if needLower and keyword == app.keyword.lower():
                    apps.append(app)
                elif not needLower and keyword == app.keyword:
                    apps.append(app)
            return apps

        regex = Search.getRegex(keyword)
        for app in AppList.getAppList():
            match = regex.search(app.keyword.lower() if needLower else app.keyword)
            if match:
                apps.append((len(match.group()), match.start(), app))
        return [x for _, _, x in sorted(apps, key=lambda x: (x[0], x[1], x[2].keyword.lower()))]

    @staticmethod
    def searchFiles(keyword):
        files = []
        needLower = isNeedLower(keyword)
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
            ret.append(FileCmd().set(name=basename(files[i]), path=files[i], iconName=getFileIconName(files[i])))
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
