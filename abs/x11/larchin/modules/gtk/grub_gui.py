# grub_gui.py - extra widgets for the grub stage
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
# 2008.06.04

import gtk

class Mbrinstall(gtk.Frame):
    """
    """
    def __init__(self, master):
        gtk.Frame.__init__(self)
        self.master = master
        self.set_border_width(20)

        vb = gtk.VBox(spacing = 10)
        hb = gtk.HBox(spacing=5)
        hb.set_border_width(5)
        vb.pack_start(hb, False)
        self.drive = gtk.combo_box_new_text()
        hb.pack_end(self.drive, False)
        hb.pack_end(gtk.Label(_("Boot Device: ")), False)
        for d in install.listDevices():
            self.drive.append_text(d[0])
        self.drive.set_active(0)

        mlcombobox = gtk.HBox(spacing=5)
        mlcombobox.set_border_width(5)
        l = gtk.Label(_("Select menu.lst to import: "))
        mlcombobox.pack_start(l, False)
        self.mlcombo = gtk.combo_box_new_text()
        self.mlcombo.connect("changed", mainWindow.sigprocess, self.newimport)
        self.mlcombo.append_text(_("None"))
        for d, p in install.menulst:
            self.mlcombo.append_text("%s:%s" % (d, p))
        mlcombobox.pack_start(self.mlcombo, False)

        eb = gtk.Button(_("Edit menu.lst"))
        eb.connect("clicked", self.editmbr)
        mlcombobox.pack_end(eb, False)

        vb.pack_start(mlcombobox, False)
        self.add(vb)
        self.show_all()

    def set_enabled(self, on):
        if on:
            self.mlcombo.set_active(0)
        else:
            self.mlcombo.set_active(-1)
        self.set_sensitive(on)
        self.newimport()

    def newimport(self, data=None):
        if (self.mlcombo.get_active() <= 0):
            at = None
        else:
            at = self.mlcombo.get_active_text()
        self.master.setimport_cb(at)

    def editmbr(self, widget, data=None):
        # Start the editor.
        self.master.editmbr_cb()

    def get_drive(self):
        return self.drive.get_active_text()


class Oldgrub(gtk.Frame):
    """
    """
    def __init__(self, master):
        gtk.Frame.__init__(self)
        self.set_border_width(20)
        self.master = master

        mlcombobox = gtk.HBox(spacing=5)
        mlcombobox.set_border_width(5)
        l = gtk.Label(_("Select menu.lst to use: "))
        mlcombobox.pack_start(l, False)
        self.mlcombo = gtk.combo_box_new_text()
        self.mlcombo.connect("changed", mainWindow.sigprocess, self.newml)
        for d, p in install.menulst:
            self.mlcombo.append_text("%s:%s" % (d, p))
        mlcombobox.pack_start(self.mlcombo, False)

        eb = gtk.Button(_("Edit menu.lst"))
        eb.connect("clicked", self.editml)
        mlcombobox.pack_end(eb, False)

        self.add(mlcombobox)
        self.set_enabled(False)
        self.show_all()

    def set_enabled(self, on):
        if on:
            self.mlcombo.set_active(0)
        else:
            self.mlcombo.set_active(-1)
        self.set_sensitive(on)
        self.newml(None)

    def newml(self, widget, data=None):
        self.master.setml_cb(self.mlcombo.get_active_text())

    def editml(self, widget, data=None):
        # Start the editor.
        self.master.editml_cb()
