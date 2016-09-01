# coding=utf-8
import glob
import os

from cmd import FileCmd
from file import getFileIconName

__author__ = 'peter'


class FileManager:
    basePath = '/'
    curPath = ''
    showHideFiles = False

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
    def getFileList(keyword):
        if keyword.startswith('~'):
            keyword = os.path.expanduser(keyword)
        keyword = ''.join(map(FileManager.either, keyword))
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
            ret.append(FileCmd().set(name=os.path.basename(f), path=f, iconName=getFileIconName(f)))
        return ret
