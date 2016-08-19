# coding=utf-8
from configparser import ConfigParser

__author__ = 'peter'


class Cfg:
    basePath = "/home/peter/src/Linalfred/"
    cfgPath = basePath + "config/"
    pluginPath = basePath + "plugins/"

    @staticmethod
    def get(sectionName, key):
        cp = ConfigParser()
        cp.read(Cfg.cfgPath + "config.ini")
        return cp.get(sectionName, key)

    @staticmethod
    def getInt(sectionName, key):
        return int(Cfg.get(sectionName, key))
