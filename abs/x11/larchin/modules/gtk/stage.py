# stage.py - base class for stages of the installer
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

import gtk, gobject

styles = {  'red' : '<span foreground="red">%s</span>'
    }

class Stage(gtk.VBox):
    def __init__(self, title):
        gtk.VBox.__init__(self)
        self.options = {}
        self.option0 = None

        # A flag to allow a stage to be skipped
        self.skip = False

        ltitle = gtk.Label()
        ltitle.set_markup('<span size="xx-large">%s</span>' % title)
        self.pack_start(ltitle, False, padding=10)

    def getHelp(self):
        return _("Sorry, I'm afraid there is at present no information"
                " for this stage.")

    def help(self):
        dialog = gtk.MessageDialog(None,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO, gtk.BUTTONS_OK)
        #dialog.set_markup("<b>%s</b>" % self.stageTitle())
        dialog.format_secondary_markup(self.getHelp())
        dialog.set_title(_("larchin Help"))
        dialog.run()
        dialog.destroy()

    def addOption(self, name, label, default=False, style=None, callback=None):
        b = gtk.RadioButton(self.option0)
        if callback:
            b.connect("toggled", self.toggled_cb, callback)

        l = gtk.Label()
        if style:
            label = styles[style] % label
        l.set_markup(label)
        b.add(l)

        self.options[name] = b
        self.pack_start(b)
        self.option0 = b
        if default:
            b.set_active(True)
        return b

    def setOption(self, item):
        for n, b in self.options.items():
            if (n == item):
                b.set_active(True)
                return

    def addCheckButton(self, label, callback=None):
        b = gtk.CheckButton(label)
        self.pack_start(b)
        if callback:
            b.connect("toggled", self.toggled_cb, callback)
        return b

    def setCheck(self, b, on):
        b.set_active(on)

    def getCheck(self, b):
        return b.get_active()

    def addLabel(self, text, align=None, style=None):
        l = gtk.Label()
        if style:
            text = styles[style] % text
        l.set_markup(text)
        l.set_line_wrap(True)
        self.pack_start(l)
        if (align == 'right'):
            l.set_alignment(1.0, 0.5)
        elif  (align == 'left'):
            l.set_alignment(0.0, 0.5)
        return l

    def setLabel(self, l, text):
        l.set_markup(text)

    def addReportWidget(self, title=None):
        w = Report()
        return self.addWidget(w)

    def addWidget(self, w, expand=True):
        self.pack_start(w, expand)
        return w

    def removeWidget(self, w):
        self.remove(w)

    def clear(self):
        for c in self.get_children():
            self.removeWidget(c)
        self.options = {}
        self.option0 = None

    def getSelectedOption(self):
        for n, b in self.options.items():
            if b.get_active():
                return n
        return None

    def toggled_cb(self, widget, callback):
        mainWindow.sigprocess(widget, callback, widget.get_active())

    # Idle callback handling
    def request_update(self, callback):
        gobject.idle_add(callback)

    def request_soon(self, callback):
        gobject.timeout_add(100, callback)

    def stop_callback(self):
        """Do 'return self.stop_callback()' at the end of a callback
        so that it is not called again in the next idle loop.
        """
        return False


class ShowInfoWidget(gtk.HBox):
    """A widget to display (only - it is not editable) one piece of
    information, a label and an entry.
    """
    def __init__(self, text):
        gtk.HBox.__init__(self)
        self.label = gtk.Label()
        self.label.set_text(text)
        self.sizew = gtk.Entry(20)
        self.sizew.set_editable(False)
        self.pack_end(self.sizew, False)
        self.pack_end(self.label, False)

    def set(self, val):
        self.sizew.set_text(val)


class Report(gtk.ScrolledWindow):
    """
    """
    def __init__(self):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.view = gtk.TextView()
        self.view.set_editable(False)
        #view.set_wrap_mode(gtk.WRAP_WORD)
        self.add(self.view)
        self.show()
        self.view.show()

        self.reportbuf = self.view.get_buffer()
        self.mark = self.reportbuf.create_mark(None,
                self.reportbuf.get_end_iter(), False)

    def report(self, text):
        self.reportbuf.insert(self.reportbuf.get_end_iter(), text+'\n')
        self.view.scroll_mark_onscreen(self.mark)
        mainWindow.eventloop()

    def backline(self):
        lc = self.reportbuf.get_line_count()
        li = self.reportbuf.get_iter_at_line(lc-2)
        ei = self.reportbuf.get_end_iter()
        self.reportbuf.delete(li, ei)

