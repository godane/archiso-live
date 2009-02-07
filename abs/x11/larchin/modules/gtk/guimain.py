#!/usr/bin/env python
#
# guimain.py - larchin main window
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

# Add a Quit button?

import gtk, gobject
from dialogs import popupError
from stage import Report

class Larchin(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_default_size(750,500)
        self.connect("destroy", self.exit)
        self.set_border_width(3)

        vbox1 = gtk.VBox()

        header = gtk.Label()
        header.set_markup('<span foreground="blue" size="20000">'
                '<i><b>larchin</b></i> %s</span>'
                % _("Installer for Arch Linux"))
        vbox1.pack_start(header, expand=False, padding=3)

        self.pane = gtk.HPaned()

        self.stageList = StageList()
        self.pane.pack1(self.stageList)
        self.pane.set_position(150)

        # The main widget for the current stage will occupy the right
        # position of the pane.
        self.mainframe = gtk.Frame()
        self.pane.pack2(self.mainframe)
        self.mainframe.set_shadow_type(gtk.SHADOW_IN)
        #self.mainframe.set_size_request(500,400)

        self.mainWidget = None

        vbox1.pack_start(self.pane)

        # The reporting window
        self.toplevel = gtk.Window()
        self.toplevel.set_title(_("larchin - log"))
        self.toplevel.connect("delete-event", self.closereport)
        self.toplevel.set_default_size(600,400)
        self.reportw = Report()
        self.toplevel.add(self.reportw)

        buttons = gtk.HBox(False, spacing=10)
        self.rButton = gtk.Button(stock=gtk.STOCK_OK)
        self.hButton = gtk.Button(stock=gtk.STOCK_HELP)
        self.oButton = gtk.ToggleButton(_("Reporting"))
        buttons.pack_start(self.hButton, False, False, padding=3)
        buttons.pack_start(self.oButton, False, False, padding=3)
        buttons.pack_end(self.rButton, False, False, padding=3)

        vbox1.pack_start(buttons, expand=False, padding=3)

        self.add(vbox1)

        self.hButton.connect("clicked", self.help)
        self.oButton.connect("toggled", self.showreport)
        self.rButton.connect("clicked", self.sigprocess, self.ok)

        self.watchcursor = gtk.gdk.Cursor(gtk.gdk.WATCH)

        self.busy = False

    #################### Dispatchers for the stage list widget
    def setStageList(self, stages):
        self.stageList.initStages(stages)

    def setStageDone(self, stagename):
        self.stageList.done(stagename)

    def selectStage(self, stagename):
        self.stageList.select(stagename)

    ###########################################################

    def mainLoop(self):
        self.show_all()
        gtk.main()

    def exit(self, widget=None, data=None):
        install.tidyup()
        gtk.main_quit()

    def closereport(self, widget, event, data=None):
        self.oButton.set_active(False)
        return True

    #def enable_forward(self, on):
    #    self.rButton.set_sensitive(on)

    def sigprocess(self, widget, slot, arg=None):
        if self.busy:
            return
        self.busy = True
        self.busy_on()

        slot(arg)

        self.busy_off()
        self.busy = False

    def busy_on(self):
        if not self.window:
            return
        self.window.set_cursor(self.watchcursor)
        self.eventloop()

    def busy_off(self):
        if not self.window:
            return
        self.window.set_cursor(None)

    def eventloop(self, t=0):
        while gtk.events_pending():
                gtk.main_iteration(False)
        if (t > 0.0):
                self.timedout = False
                gobject.timeout_add(int(t*1000), self.timeout)
                while not self.timedout:
                    gtk.main_iteration(True)

    def timeout(self):
        self.timedout = True
        # Cancel this timer
        return False

    def setStage(self, stagename):
        self.busy_on()
        current = self.mainframe.get_child()
        if current:
            self.mainframe.remove(current)

        self.mainWidget = stages[stagename].Widget()
        self.mainWidget.stagename = stagename
        if self.mainWidget.skip:
            self.ok('notdone')
        else:
            self.mainframe.add(self.mainWidget)
            self.mainWidget.show_all()

        self.busy_off()
        self.eventloop()

    def help(self, widget, data=None):
        self.mainWidget.help()

    def showreport(self, widget, data=None):
        if widget.get_active():
            self.toplevel.show_all()
        else:
            self.toplevel.hide_all()

    def ok(self, data):
        stagename = self.mainWidget.stagename
        rval = self.mainWidget.forward()
        if (rval < 0):
            return
        if (data != 'notdone'):
            self.setStageDone(stagename)
        self.selectStage(stageSwitch[stagename][rval])

class StageList(gtk.ScrolledWindow):
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type(gtk.SHADOW_IN)

        self.treeview = gtk.TreeView()
        # The list model columns are:
        #   stage name
        #   displayed string
        #   completed flag
        self.liststore = gtk.ListStore(str, str, bool)
        self.treeview.set_model(self.liststore)
        # create CellRenderers to render the data
        celltoggle = gtk.CellRendererToggle()
        celltext = gtk.CellRendererText()
        cellcurrent = gtk.CellRendererText()
        # create the TreeViewColumn to display the groups
        self.tvcolumn = gtk.TreeViewColumn(_("Stages"))
        self.tvcolumn.pack_start(celltoggle, expand=False)
        self.tvcolumn.add_attribute(celltoggle, 'active', 2)
        self.tvcolumn.pack_start(celltext, expand=True)
        self.tvcolumn.add_attribute(celltext, 'markup', 1)
        # add column to treeview
        self.treeview.append_column(self.tvcolumn)
        self.add(self.treeview)

        self.selection = self.treeview.get_selection()
        self.selection.set_mode(gtk.SELECTION_SINGLE)
        self.selection.connect('changed', self.changed_cb)

    def initStages(self, stages):
        self.liststore.clear()
        for sn, st in stages:
            self.liststore.append([sn, st, False])

    def done(self, stagename):
        i = 0
        for r in self.liststore:
            if (r[0] == stagename):
                self.liststore[i][2] = True
                break
            i += 1

    def select(self, stagename):
        i = 0
        for r in self.liststore:
            if (r[0] == stagename):
                self.selection.select_path(i)
                return
            i += 1

        if (stagename == '/'):
            mainWindow.exit()
        else:
            popupError(_("Attempt to select non-existent stage: %s") %
                    stagename, "BUG")

    def changed_cb(self, widget, data=None):
        tv, iter = self.selection.get_selected()
        if iter:
            s = self.liststore.get_value(iter, 0)
            mainWindow.setStage(s)


