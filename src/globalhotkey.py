# coding=utf-8
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from Xlib.display import Display
from Xlib import X, error

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

__author__ = 'peter'


class HotKey:
    def __init__(self):
        self.keyVal = None
        self.keyCode = None
        self.modifiers = None
        self.wait_for_release = False

    def set(self, keyVal=None, keyCode=None, modifiers=None):
        if keyVal:
            self.keyVal = keyVal
        if keyCode:
            self.keyCode = keyCode
        if modifiers:
            self.modifiers = modifiers
        return self


class GlobalHotKeyBinding(QThread):
    keyPressSignal = pyqtSignal(object)

    def __init__(self, parent=None, callBack=None):
        super().__init__(parent)
        self.dlg = parent
        self.keymap = Gdk.Keymap.get_default()
        self.display = Display()
        self.screen = self.display.screen()
        self.root = self.screen.root
        self.map_modifiers()
        self.hotKeyList = []
        self.running = False
        self.keyPressSignal.connect(callBack)

    def map_modifiers(self):
        gdk_modifiers = (Gdk.ModifierType.CONTROL_MASK, Gdk.ModifierType.SHIFT_MASK, Gdk.ModifierType.MOD1_MASK,
                         Gdk.ModifierType.MOD2_MASK, Gdk.ModifierType.MOD3_MASK, Gdk.ModifierType.MOD4_MASK,
                         Gdk.ModifierType.MOD5_MASK, Gdk.ModifierType.SUPER_MASK, Gdk.ModifierType.HYPER_MASK)
        self.known_modifiers_mask = 0
        for modifier in gdk_modifiers:
            if "Mod" not in Gtk.accelerator_name(0, modifier):
                self.known_modifiers_mask |= modifier

    def grab(self, accelerator):
        keyVal, modifiers = Gtk.accelerator_parse(accelerator)
        if not accelerator or (not keyVal and not modifiers):
            return

        keyCode = self.keymap.get_entries_for_keyval(keyVal)[1][0].keycode
        modifiers = int(modifiers)

        catch = error.CatchError(error.BadAccess)
        self.root.grab_key(keyCode, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeSync, onerror=catch)
        if catch.get_error():
            return False
        self.hotKeyList.append(HotKey().set(keyVal=keyVal, keyCode=keyCode, modifiers=modifiers))
        return True

    def ungrab_all(self):
        for hotKey in self.hotKeyList:
            self.root.ungrab_key(hotKey.keyCode, X.AnyModifier, self.root)

    def run(self):
        self.running = True
        while self.running:
            event = self.display.next_event()
            print(event)
            if event is None or not hasattr(event, 'detail'):
                # self.display.allow_events(X.ReplayKeyboard, event.time)
                continue
            for hotKey in self.hotKeyList:
                if event.detail == hotKey.keyCode and event.type == X.KeyPress and not hotKey.wait_for_release:
                    modifiers = event.state & self.known_modifiers_mask
                    if modifiers == hotKey.modifiers:
                        hotKey.wait_for_release = True
                        self.display.allow_events(X.AsyncKeyboard, event.time)
                        break
                elif event.detail == hotKey.keyCode and hotKey.wait_for_release:
                    if event.type == X.KeyRelease:
                        hotKey.wait_for_release = False
                        self.dlg.mutexThread.lock()
                        self.keyPressSignal.emit(hotKey)
                        self.dlg.mutexThread.unlock()
                    self.display.allow_events(X.AsyncKeyboard, event.time)
                    break
            else:
                self.display.allow_events(X.ReplayKeyboard, event.time)

    def stop(self):
        self.running = False
        self.ungrab_all()
        self.display.close()
