# coding=utf-8
import glob
import os

from PyQt5.QtCore import QProcess

from cmd import Cmd, CmdType
from file import getFileIconName
from plugin_common.baseplugin import RetVal

__author__ = 'peter'


class FileManagerCmd(Cmd):
    def __init__(self):
        super().__init__()
        self.type = CmdType.fileManager
        self.path = None

    def getDesc(self):
        return self.keyword

    def exec(self, cmd):
        # QProcess.startDetached('xdg-open', [self.path])
        return RetVal.cmd + self.complement(cmd)

    def set(self, name=None, keyword=None, path=None, iconName=None):
        self.name = name
        if keyword:
            self.keyword = keyword
        else:
            self.keyword = self.name
        self.path = path
        self.iconName = iconName
        return self

    def complement(self, cmd):
        if os.path.isdir(self.path):
            return self.keyword + '/'
        else:
            return self.keyword


class FileManager:
    basePath = '/'
    curPath = ''
    showHideFiles = False

    @staticmethod
    def getHomePath():
        return os.path.expanduser('~') + '/'

    @staticmethod
    def setBasePath(path):
        if path == '/':
            FileManager.basePath = '/'
        elif path == '~':
            FileManager.basePath = os.path.expanduser('~') + '/'

    @staticmethod
    def either(c):
        return '[%s%s]*' % (c.lower(), c.upper()) if c.isalpha() else c

    @staticmethod
    def collapsePath(path):
        if path.startswith(FileManager.getHomePath()):
            return path.replace(FileManager.getHomePath(), '~/', 1)
        else:
            return path

    @staticmethod
    def expandPath(path):
        return os.path.expanduser(path)

    @staticmethod
    def getFileList(keyword):
        keyword = ''.join(map(FileManager.either, keyword))
        print(keyword)
        keyword = os.path.expanduser(keyword)
        print(keyword)
        if keyword.endswith('/'):
            return glob.glob(keyword + '*')
        elif keyword.endswith('?') or keyword.endswith('*'):
            return glob.glob(keyword)
        else:
            return glob.glob(keyword + '*')

    @staticmethod
    def Search(keyword):
        ret = []
        for f in sorted(FileManager.getFileList(keyword)):
            ret.append(FileManagerCmd().set(name=os.path.basename(f), path=f,
                                            keyword=FileManager.collapsePath(f),
                                            iconName=getFileIconName(f)))
        return ret
