# coding=utf-8
import re

from os.path import basename

from app import AppList
from cmd import FileCmd, BuildInCmdList
from common import isNeedLower, isSmartEqual, isSmartStartsWith
from config import Cfg
from file import getFileList, getFileIconName
from plugin import Plugin

__author__ = 'peter'


class Search:
    @staticmethod
    def smartCompare(text1, text2, needLower):
        if needLower and text1 == text2.lower():
            return True
        elif not needLower and text1 == text2:
            return True
        return False

    @staticmethod
    def getRegex(keyword):
        pattern = '.*?'.join(keyword)
        return re.compile(pattern)

    @staticmethod
    def searchApps(keyword):
        apps = []
        needLower = isNeedLower(keyword)

        # 如果命令中有空格,优先精确搜索
        if ' ' in keyword:
            for app in AppList.getAppList() + Plugin.getPluginList() + BuildInCmdList.getList():
                if isSmartStartsWith(keyword, app.keyword):
                    apps.append(app)
            if len(apps) == 1:
                return apps[0].list(keyword)

        regex = Search.getRegex(keyword)
        for app in AppList.getAppList() + Plugin.getPluginList() + BuildInCmdList.getList():
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
            ret = Search.searchApps(keyword)
        return ret
