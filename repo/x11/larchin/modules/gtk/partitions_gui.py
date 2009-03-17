# partitions_gui.py - extra widgets for the partitions stage
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

class PartitionWidget(gtk.Frame):
    """This widget is for partition creation.
    The creation can be optional (checkbox) and the size can be set
    by a slider.
    When the partition is not created, a notice will be shown instead of
    the slider.
    """
    def __init__(self, title_size, title_checkbutton, notice_off, size_cb):
        gtk.Frame.__init__(self)
        self.size_callback = size_cb
        adjlabel = gtk.Label(title_size)
        adjlabel.set_alignment(0.9, 0.5)
        self.adj = gtk.Adjustment(lower=0.1, step_incr=0.1, page_incr=1.0)
        hscale = gtk.HScale(self.adj)

        self.onSwitch = gtk.CheckButton(title_checkbutton)

        self.set_label_widget(self.onSwitch)
        self.box = gtk.VBox()
        self.box.pack_start(adjlabel)
        self.box.pack_start(hscale)

        self.notice = gtk.Label(notice_off)
        self.notice.set_line_wrap(True)

        self.add(self.box)

        self.onstate = False
        self.adj.connect("value_changed", self.new_size_cb)
        self.onSwitch.connect("toggled", self.check_cb)

    def new_size_cb(self, widget, data=None):
        self.size_callback(self.adj.value)

    def check_cb(self, widget, data=None):
        self.set_on(self.onSwitch.get_active(), False)

    def set_on(self, on, update=True):
        if (on != self.onstate):
            self.onstate = on
        if on:
            widget = self.box
            self.size_callback(self.adj.value)
        else:
            widget = self.notice
            self.size_callback(0.0)
        if update:
            self.onSwitch.set_active(on)
        else:
            child = self.get_child()
            if child:
                self.remove(child)
            self.add(widget)
            widget.show()

    def set_adjust(self, lower = None, upper = None,
            value = None, update = True):
        """Set the size adjustment slider. Any of lower limit, upper limit
        and size can be set independently.
        """
        if (lower != None):
            self.adj.lower = lower
        if (upper != None):
            self.adj.upper = upper
        if ((value != None)
                and (value >= self.adj.lower)
                and (value <= self.adj.upper)):
            self.adj.value = value

