#!/usr/bin/env python

# progress status indicator

import pygtk
pygtk.require('2.0')
import gtk, gobject, os, sys

class ProgressBar:
    # Callback that toggles the text display within the progress
    # bar trough
    # Update the value of the progress bar so that we get
    # some movement
    def progress_timeout(self, pbobj):
        if (os.path.exists('/tmp/run')):
	    pbobj.pbar.pulse()
        else:
	    self.destroy_progress(None)
    # As this is a timeout function, return TRUE so that it
    # continues to get called
        return True

    def toggle_show_text(self, widget, data=None):
        if widget.get_active():
            self.pbar.set_text("some text")
        else:
            self.pbar.set_text("")

    # Clean up allocated memory and remove the timer
    def destroy_progress(self, widget, data=None):
        gobject.source_remove(self.timer)
        self.timer = 0
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)

        self.window.connect("destroy", self.destroy_progress)
        self.window.set_title(sys.argv[1])
        self.window.set_border_width(0)

        vbox = gtk.VBox(False, 5)
        vbox.set_border_width(10)
        self.window.add(vbox)
        vbox.show()
	
	label = gtk.Label("This may take a minute or so\n\
depending on your hardware.")
        vbox.pack_start(label, False, False, 0)
	label.show()
        # Create a centering alignment object
        align = gtk.Alignment(0.5, 0.5, 0, 0)
        vbox.pack_start(align, False, False, 5)
        align.show()

        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()
        self.pbar.set_size_request(320, 20)
        align.add(self.pbar)
        self.pbar.show()

        # Add a timer callback to update the value of the progress bar
        self.timer = gobject.timeout_add (100, self.progress_timeout, self)

        self.window.show()

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ProgressBar()
    main()
