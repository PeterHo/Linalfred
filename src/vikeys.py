# coding=utf-8
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

__author__ = 'peter'


def onUp(globalhotkey):
    globalhotkey.send_key('Up')


def onDown(globalhotkey):
    globalhotkey.send_key('Down')


def onLeft(globalhotkey):
    globalhotkey.send_key('Left')


def onRight(globalhotkey):
    globalhotkey.send_key('Right')


def onPageUp(globalhotkey):
    globalhotkey.send_key('Page_Up')


def onPageDown(globalhotkey):
    globalhotkey.send_key('Page_Down')


hotKeys = [
    ('<Mod4>J', onDown),
    ('<Mod4>K', onUp),
    ('<Mod4>H', onLeft),
    ('<Mod4>L', onRight),
    ('<Mod4>U', onPageDown),
    ('<Mod4>I', onPageUp),
]


def onViKeys(globalhotkey, hotkey):
    for key in hotKeys:
        keyVal, modifiers = Gtk.accelerator_parse(key[0])
        if keyVal == hotkey.keyVal and modifiers == hotkey.modifiers:
            key[1](globalhotkey)
            return True
    return False


def addViKeysHotKeys(key):
    for hotkey in hotKeys:
        key.grab(hotkey[0])
