# coding=utf-8
import time

from PyQt5.QtCore import QThread
from Xlib.display import Display
from Xlib import X, XK, protocol, error

import gi

from switchwnd import onSwitchWnd, addSwitchWndHotKeys
from vikeys import addViKeysHotKeys, onViKeys

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
    def __init__(self, parent=None, callBack=None):
        super().__init__(parent)
        self.dlg = parent
        self.keymap = Gdk.Keymap.get_default()
        self.display = Display()
        self.screen = self.display.screen()
        self.root = self.screen.root
        self.ignored_masks = self.get_mask_combinations(X.LockMask | X.Mod2Mask | X.Mod5Mask)
        self.map_modifiers()
        self.hotKeyList = []
        self.running = False
        self.callBack = callBack

    def get_mask_combinations(self, mask):
        return [x for x in range(mask + 1) if not (x & ~mask)]

    def map_modifiers(self):
        gdk_modifiers = (Gdk.ModifierType.CONTROL_MASK, Gdk.ModifierType.SHIFT_MASK, Gdk.ModifierType.MOD1_MASK,
                         # Gdk.ModifierType.MOD2_MASK, Gdk.ModifierType.MOD3_MASK,
                         Gdk.ModifierType.MOD4_MASK,
                         # Gdk.ModifierType.MOD5_MASK,
                         Gdk.ModifierType.SUPER_MASK, Gdk.ModifierType.HYPER_MASK)
        self.known_modifiers_mask = 0
        for modifier in gdk_modifiers:
            # if "Mod" not in Gtk.accelerator_name(0, modifier):
            self.known_modifiers_mask |= modifier

    def grab(self, accelerator):
        keyVal, modifiers = Gtk.accelerator_parse(accelerator)
        if not accelerator or (not keyVal and not modifiers):
            return

        keyCode = self.keymap.get_entries_for_keyval(keyVal)[1][0].keycode
        modifiers = int(modifiers)

        catch = error.CatchError(error.BadAccess)
        for ignored_mask in self.ignored_masks:
            mod = modifiers | ignored_mask
            self.root.grab_key(keyCode, mod, True, X.GrabModeAsync, X.GrabModeSync, onerror=catch)
        self.display.sync()
        if catch.get_error():
            return False
        self.hotKeyList.append(HotKey().set(keyVal=keyVal, keyCode=keyCode, modifiers=modifiers))
        return True

    def ungrab_all(self):
        for hotKey in self.hotKeyList:
            self.root.ungrab_key(hotKey.keyCode, X.AnyModifier, self.root)

    def send_key(self, emulated_key):
        shift_mask = 0  # or Xlib.X.ShiftMask
        window = self.display.get_input_focus()._data["focus"]
        keysym = XK.string_to_keysym(emulated_key)
        keycode = self.display.keysym_to_keycode(keysym)
        event = protocol.event.KeyPress(
            time=int(time.time()),
            root=self.root,
            window=window,
            same_screen=0, child=X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=shift_mask,
            detail=keycode
        )
        window.send_event(event, propagate=True)
        event = protocol.event.KeyRelease(
            time=int(time.time()),
            root=self.display.screen().root,
            window=window,
            same_screen=0, child=X.NONE,
            root_x=0, root_y=0, event_x=0, event_y=0,
            state=shift_mask,
            detail=keycode
        )
        window.send_event(event, propagate=True)

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
                        self.callBack(self, hotKey)
                        self.dlg.mutexThread.unlock()
                    self.display.allow_events(X.AsyncKeyboard, event.time)
                    break
            else:
                self.display.allow_events(X.ReplayKeyboard, event.time)

    def stop(self):
        self.running = False
        self.ungrab_all()
        self.display.close()


def onGlobalHotKey(obj, hotkey):
    if onSwitchWnd(hotkey):
        return
    if onViKeys(obj, hotkey):
        return


def initGlobalHotKey(dlg):
    key = GlobalHotKeyBinding(dlg, onGlobalHotKey)
    addViKeysHotKeys(key)
    addSwitchWndHotKeys(key)
    key.start()
