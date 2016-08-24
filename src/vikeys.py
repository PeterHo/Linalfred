# coding=utf-8
from virtkey import virtkey

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

__author__ = 'peter'


def onUp():
    v = virtkey()
    v.press_keysym(65362)
    v.release_keysym(65362)


def onDown():
    v = virtkey()
    v.press_keysym(65364)
    v.release_keysym(65364)


def onLeft():
    v = virtkey()
    v.press_keysym(65361)
    v.release_keysym(65361)


def onRight():
    v = virtkey()
    v.press_keysym(65363)
    v.release_keysym(65363)


def onPageUp():
    v = virtkey()
    v.press_keysym(65365)
    v.release_keysym(65365)


def onPageDown():
    v = virtkey()
    v.press_keysym(65366)
    v.release_keysym(65366)


hotKeys = [
    ('<Mod4>J', onDown),
    ('<Mod4>K', onUp),
    ('<Mod4>H', onLeft),
    ('<Mod4>L', onRight),
    ('<Mod4>U', onPageDown),
    ('<Mod4>I', onPageUp),
]


def onViKeys(hotkey):
    for key in hotKeys:
        keyVal, modifiers = Gtk.accelerator_parse(key[0])
        if keyVal == hotkey.keyVal and modifiers == hotkey.modifiers:
            key[1]()
            return True
    return False


def addViKeysHotKeys(key):
    for hotkey in hotKeys:
        key.grab(hotkey[0])
