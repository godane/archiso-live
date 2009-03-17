# rootpw_gui.py - extra widgets for the root password stage
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
# 2008.06.05

import gtk

class PWEnter(gtk.Table):
    """A widget for entering a password, with double entry.
    """
    def __init__(self):
        gtk.Table.__init__(self, 2, 2)
        self.set_row_spacings(10)

        l1 = gtk.Label(_("Enter new root password:"))
        l1.set_alignment(1.0, 0.5)
        self.attach(l1, 0, 1, 0, 1,
                xoptions=gtk.FILL, yoptions=gtk.FILL,
                xpadding=5, ypadding=5)
        self.pw1 = gtk.Entry()
        self.pw1.set_visibility(False)
        self.attach(self.pw1, 1, 2, 0, 1,
                xoptions=gtk.FILL|gtk.EXPAND, yoptions=gtk.FILL|gtk.EXPAND,
                xpadding=5, ypadding=5)

        l2 = gtk.Label(_("Reenter new root password:"))
        l2.set_alignment(1.0, 0.5)
        self.attach(l2, 0, 1, 1, 2,
                xoptions=gtk.FILL, yoptions=gtk.FILL,
                xpadding=5, ypadding=5)
        self.pw2 = gtk.Entry()
        self.pw2.set_visibility(False)
        self.attach(self.pw2, 1, 2, 1, 2,
                xoptions=gtk.FILL|gtk.EXPAND, yoptions=gtk.FILL|gtk.EXPAND,
                xpadding=5, ypadding=5)

    def get_text1(self):
        return self.pw1.get_text()

    def get_text2(self):
        return self.pw2.get_text()

    def move_focus(self):
        """This is a 'request_soon' callback, so it needs to return
        False to stop it being called again.
        """
        self.pw1.grab_focus()
        return False
