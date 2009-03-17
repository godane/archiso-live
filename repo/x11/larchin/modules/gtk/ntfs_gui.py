# ntfs_gui.py - extra widgets for the ntfs stage
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
# 2008.06.03

import gtk

from stage import ShowInfoWidget

class NtfsWidget(gtk.Frame):
    """This widget allows an existing operating system (Windows/NTFS only)
    partition to be shrunk or deleted (or retained unchanged).
    """
    def __init__(self, changed_cb):
        self.size_cb = changed_cb

        gtk.Frame.__init__(self)
        self.set_border_width(5)

        self.delbt = gtk.CheckButton(_("Delete this partition"))
        self.set_label_widget(self.delbt)

        self.dlabel = gtk.Label(_("WARNING: All data on this partition"
                " will be lost"))

        adjlabel = gtk.Label(_("Set new size of NTFS partition (GB)"))
        adjlabel.set_alignment(0.9, 0.5)
        self.ntfsadj = gtk.Adjustment(step_incr=0.1, page_incr=1.0)
        hscale = gtk.HScale(self.ntfsadj)

        self.shrink = gtk.CheckButton(_("Shrink NTFS partition"))

        self.rlabel = gtk.Label()   # To display when not shrinking

        self.ntfsframe = gtk.Frame()
        self.ntfsframe.set_border_width(10)
        self.ntfsframe.set_label_widget(self.shrink)
        self.ntfsbox = gtk.VBox()
        self.ntfsbox.pack_start(adjlabel)
        self.ntfsbox.pack_start(hscale)

        self.deletestate = False
        self.shrinkstate = False
        self.toofullstate = False
        self.size = 0.0
        self.min = 0.0
        self.max = 0.0

        self.ntfsadj.connect("value_changed", self.ntfs_size_cb)
        self.shrink.connect("toggled", self.shrink_check_cb)
        self.delbt.connect("toggled", self.del_check_cb)

    def set_delete(self, on, update=True):
        """Set checkbutton 'delete partition' on or off.
        """
        self.deletestate = on
        child = self.get_child()
        if child:
            self.remove(child)
        if on:
            self.add(self.dlabel)
            self.dlabel.show()
            self.size_cb(-1)
        else:
            self.add(self.ntfsframe)
            self.ntfsframe.show_all()
            self.set_shrink(self.shrinkstate, update)
        if update:
            self.delbt.set_active(on)

    def toofull(self, on):
        self.toofullstate = on

    def del_check_cb(self, widget, data=None):
        self.set_delete(self.delbt.get_active(), False)

    def set_shrink(self, on, update=True):
        """Set checkbutton 'shrink partition' on or off.
        """
        self.shrinkstate = on
        self.shrink.set_sensitive(not self.toofullstate)
        if self.toofullstate:
            self.shrinkstate = False

        child = self.ntfsframe.get_child()
        if child:
            self.ntfsframe.remove(child)
        if on:
            self.ntfsframe.add(self.ntfsbox)
            self.ntfsbox.show_all()
            self.size_cb(self.size)
        else:
            self.ntfsframe.add(self.rlabel)
            rlabeltext = (_("This partition (size %s)"
                    " will be retained unchanged") % self.partsize)
            if self.toofullstate:
                rlabeltext = (_("This partition is too full to shrink\n\n")
                        + rlabeltext)
            self.rlabel.set_label(rlabeltext)
            self.rlabel.show()
            self.size_cb(0)
        if update:
            self.shrink.set_active(on)

    def set_partsize(self, size):
        self.partsize = size

    def shrink_check_cb(self, widget, data=None):
        self.set_shrink(self.shrink.get_active(), False)

    def set_shrinkadjust(self, lower = None, upper = None,
            value = None, update = True):
        """Set the size adjustment slider. Any of lower limit, upper limit
        and size can be set independently.
        """
        if (lower != None):
            self.ntfsadj.lower = lower
            if (self.size < lower):
                self.size = lower
                self.ntfsadj.value = lower
        if (upper != None):
            self.ntfsadj.upper = upper
            if (self.size > upper):
                self.size = upper
                self.ntfsadj.value = upper
        if ((value != None) and (value != self.size)
                and (value >= self.ntfsadj.lower)
                and (value <= self.ntfsadj.upper)):
            self.size = value
            if self.shrinkstate and not self.deletestate:
                self.size_cb(self.size)
            if update:
                self.ntfsadj.value = value

    def ntfs_size_cb(self, widget, data=None):
        self.set_shrinkadjust(value=self.ntfsadj.value, update=False)

    def set_max(self, val):
        self.max = val
        self.set_shrinkadjust(upper=self.max)

    def set_min(self, val):
        self.min = val
        self.set_shrinkadjust(lower=self.min)

    def set_size(self, val):
        self.set_shrinkadjust(value=val)


class PartitionWidget(gtk.HBox):
    """Combined widget showing all ntfs partitions in a list,
    the currently selected one and the total disk size.
    """
    def __init__(self):
        gtk.HBox.__init__(self)

        self.plist = SimpleList(_("NTFS Partitions"))
        self.pack_start(self.plist)

        vbox = gtk.VBox()
        self.pack_end(vbox)

        # Info: partition
        self.partition = ShowInfoWidget(_("NTFS Partition:  "))
        vbox.pack_start(self.partition)

        # Info: total drive size
        self.totalsize = ShowInfoWidget(_("Total capacity of drive:  "))
        vbox.pack_start(self.totalsize)

    def set_plist(self, partlist):
        self.plist.set(partlist)

    def set_disksize(self, gb):
        self.totalsize.set(gb)

    def set_part(self, part):
        self.partition.set(part)
        self.plist.set_select(part)


class SimpleList(gtk.ScrolledWindow):
    def __init__(self, title):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_IN)

        self.treeview = gtk.TreeView()
        self.liststore = gtk.ListStore(str)
        self.treeview.set_model(self.liststore)
        # create CellRenderer to render the data
        celltext = gtk.CellRendererText()
        # create the TreeViewColumn to display the info
        self.tvcolumn = gtk.TreeViewColumn(title)
        self.tvcolumn.pack_start(celltext, expand=True)
        self.tvcolumn.add_attribute(celltext, 'text', 0)
        # add column to treeview
        self.treeview.append_column(self.tvcolumn)
        self.add(self.treeview)

        self.selection = self.treeview.get_selection()
        self.selection.set_mode(gtk.SELECTION_NONE)
        self.set_size_request(100,150)

    def set(self, tlist):
        self.liststore.clear()
        for t in tlist:
            self.liststore.append([t])

    def set_select(self, part):
        for r in self.liststore:
            if (part == r[0]):
                r[0] = part + "   <--"
                break
