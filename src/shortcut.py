# coding=utf-8
from PyQt5.QtCore import Qt

from config import Cfg

__author__ = 'peter'


class ListShortcut:
    charKeyList = ['Q', 'W', 'E',
                   'A', 'S', 'D',
                   'Z', 'X', 'C']

    numKeyList = ['1', '2', '3',
                  '4', '5', '6',
                  '7', '8', '9']

    if Cfg.get('shortcut', 'listModifier').lower() == 'alt':
        modifier = Qt.AltModifier
        modifierText = 'Alt'
    else:
        modifier = Qt.AltModifier
        modifierText = 'Alt'

    if Cfg.get('shortcut', 'listKeyType').lower() == 'char':
        keyList = charKeyList
    elif Cfg.get('shortcut', 'listKeyType').lower() == 'Num':
        keyList = numKeyList
    else:
        keyList = numKeyList

    @staticmethod
    def getShortcutText(index):
        return ListShortcut.modifierText + "+" + ListShortcut.keyList[index]

    @staticmethod
    def getShortcutKey(index):
        return ord(ListShortcut.keyList[index])

    @staticmethod
    def getModifier(index):
        return ListShortcut.modifier
