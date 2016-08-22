# coding=utf-8
import re

from os.path import basename

from app import AppList
from cmd import FileCmd, BuildInCmdList
from common import isNeedLower
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

        regex = Search.getRegex(keyword)
        for app in AppList.getAppList() + Plugin.getPluginList() + BuildInCmdList.getList():
            match = regex.search(app.keyword.lower() if needLower else app.keyword)
            if match:
                apps.append((len(match.group()), match.start(), app))
        return [x for _, _, x in sorted(apps, key=lambda x: (x[0], x[1], x[2].keyword.lower()))]

    @staticmethod
    def searchAppWithParam(keyword):
        apps = []
        cmd = keyword.split()[0]
        needLower = isNeedLower(cmd)
        # 优先搜索内置命令
        for app in BuildInCmdList.getList():
            if Search.smartCompare(cmd, app.keyword, needLower):
                # 获得内置命令的返回结果
                return app.list(keyword)

        # 再搜索插件
        for app in Plugin.getPluginList():
            if Search.smartCompare(cmd, app.keyword, needLower):
                # 获得插件的返回结果
                return app.list(keyword)

        # 最后搜索应用程序
        for app in AppList.getAppList():
            if needLower and cmd == app.keyword.lower():
                apps.append(app)
            elif not needLower and cmd == app.keyword:
                apps.append(app)
        return apps

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
            if ' ' in keyword:
                # 带参数方式的查找App,插件,内置命令
                ret = Search.searchAppWithParam(keyword)
            else:
                # 查找App,插件,内置命令
                ret = Search.searchApps(keyword)
        return ret
