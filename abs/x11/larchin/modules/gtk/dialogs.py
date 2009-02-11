#!/usr/bin/env python
#
# dialogs.py - popup dialogs for larchin
#
# (c) Copyright 2008 Michael Towers <gradgrind[at]online[dot]de>
#
# This file is part of the larch project.
#
#    larch is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    larch is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with larch; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#----------------------------------------------------------------------------
# 2008.02.12

import gtk

def popupError(text, title=""):
    dialog = gtk.MessageDialog(None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
            title)
    dialog.format_secondary_text(text)
    dialog.set_title(_("larchin Error"))
    dialog.run()
    dialog.destroy()

def popupMessage(text, title=""):
    dialog = gtk.MessageDialog(None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
            title)
    dialog.format_secondary_markup(text)
    dialog.set_title(_("larchin"))
    dialog.run()
    dialog.destroy()

def popupWarning(text, title=""):
    dialog = gtk.MessageDialog(None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
            gtk.MESSAGE_WARNING, gtk.BUTTONS_YES_NO,
            title)
    dialog.format_secondary_markup(text)
    dialog.set_title(_("larchin"))
    res = (dialog.run() == gtk.RESPONSE_YES )
    dialog.destroy()
    return res

class PopupInfo:
    def __init__(self, text, title=""):
        self.popup = gtk.MessageDialog(None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_NONE,
                title)
        self.popup.format_secondary_markup(text)
        self.popup.set_title(_("larchin"))
        self.popup.show()
        mainWindow.eventloop()

    def drop(self):
        self.popup.destroy()

def popupEditor(title, text, revert_cb=None):
    """A simple popup text editor with just three buttons:
            ok: return the text
            revert: refetch the 'original' text
            cancel: return None
    The reversion is handled by means of a callback, which must be
    supplied by the user, and is optional.
    """
    dialog = gtk.Dialog(title, None,
            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT)
    if revert_cb:
        dialog.add_button(gtk.STOCK_REVERT_TO_SAVED, gtk.RESPONSE_REJECT)
    dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
    dialog.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)

    sw = gtk.ScrolledWindow()
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    textview = gtk.TextView()
    buffer = textview.get_buffer()
    sw.add(textview)
    sw.show_all()
    sw.set_size_request(600, 400)
    dialog.vbox.pack_start(sw)

    buffer.set_text(text)

    while True:
        res = dialog.run()
        if (res == gtk.RESPONSE_REJECT):
            dialog.set_sensitive(False)
            buffer.set_text(revert_cb())
            dialog.set_sensitive(True)
        else:
            break

    if (res == gtk.RESPONSE_ACCEPT):
        res = buffer.get_text(*buffer.get_bounds())
    else:
        res = None
    dialog.destroy()
    return res

