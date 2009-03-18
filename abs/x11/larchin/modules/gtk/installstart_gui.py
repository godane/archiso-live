# installstart_gui.py - widgets for installstart stage
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

class PartTable(gtk.TreeView):
    """This widget presents a list of partitions to be formatted and/or
    mounted for the installation.
    """
    def __init__(self, plist):
        gtk.TreeView.__init__(self)

        liststore = gtk.ListStore(str, str, str, str, str, str)
        self.set_model(liststore)
        cellr = gtk.CellRendererText()

        for head, i in ((_("Partition"), 1), (_("Mount Point"), 0),
                (_("Size"), 5), (_("Format"), 2),
                (_("Fmt Flags"), 3), (_("Mnt Flags"), 4)):
            treeviewcolumn = gtk.TreeViewColumn(head, cellr, text=i)
            treeviewcolumn.set_expand(True)
            self.append_column(treeviewcolumn)

        for p in plist:
            liststore.append(p)

