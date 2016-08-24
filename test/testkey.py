# coding=utf-8

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


def catch_button(window, event, label):
    keyval = event.keyval
    name = Gdk.keyval_name(keyval)
    print(event.state)
    mod = Gtk.accelerator_get_label(keyval, event.state)
    label.set_markup('<span size="xx-large">%s\n%d</span>' % (mod, keyval))


window = Gtk.Window()
window.set_size_request(640, 480)
label = Gtk.Label()
label.set_use_markup(True)
window.connect('key-press-event', catch_button, label)
window.connect('destroy', Gtk.main_quit)
window.add(label)
window.show_all()

Gtk.main()
