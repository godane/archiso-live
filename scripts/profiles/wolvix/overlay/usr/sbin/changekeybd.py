#!/usr/bin/env python
#
# Program to install Wolvix to hard disk
#
# License:	GNU General Public license
# Author: 	Chris Gallienne
#
# Note: This script was wholly written by me, but I have lifted ideas
# from various other installer shell scripts, principally the following:
#
# DamnSmallLinux dsl-hdinstall script, which was itself a modification 
# of the KNOPPIX knx-hdinstall 0.37 by Christian Perle; the knoppix
# scripts 'knoppix-installer' by Fabian Franz and 'mkboot' by Guy Maor;
# and the 'slax-installer' scripts by Thomas Matejicek. Thomas' slax-liloconfig
# shell script has been translated almost in its entirety and adapted here
# as the function 'lilo_config'. Thanks, Thomas!
#

import pygtk
pygtk.require('2.0')
import gtk, gobject, os, sys, time

def change_keybd(data=None):
	
	def close_window (self):
		window.destroy()
	
	def key_change (self):
		os.system('/usr/X11R6/bin/setxkbmap %s' %kbdsel.get_active_text())
		if (button1.get_active()):
			keyname=''
			newline=''
			file = open('/etc/X11/xorg.conf')
			xconf = file.read()
			file.close()
			lines = xconf.split("\n", sys.maxint)
			for line in lines:
				if (line.count('InputDevice') and line.count('"CoreKeyboard"')):
					words = line.split(None, sys.maxint)
					keyname = words[1]
			file = open('/etc/X11/xorg.conf')
			xconf = file.read()
			file.close()
			newlines = xconf.split("\n", sys.maxint)
			os.unlink("/etc/X11/xorg.conf")
			file = open("/etc/X11/xorg.conf", 'w')
			found = False
			index = 0
			for line in newlines:
				if (line.count('     Option   "XkbLayout"')):
					line = ''
				file.write("%s\n" % line)	
				index = index + 1
				if (found):
					newline = '     Option   "XkbLayout"   "%s"\n' % kbdsel.get_active_text()
					file.write(newline)
					found = False
				if (line.count("Identifier") and line.count(keyname)):
					found = True
			file.close()
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
			"Keyboard Layout has been changed")
			resp = message.run()
			message.destroy()
			close_window(self)
			
	window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.set_size_request(380, 380)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_resizable(True)

        window.connect("destroy", close_window)
        window.set_title("Wolvix - Keyboard Setup")
        window.set_border_width(10)

        mainbox = gtk.VBox(False, 10)
        topbox = gtk.HBox(False, 10)
	leftbox = gtk.VBox(False, 10)
	rightbox = gtk.VBox(False, 10)
	bottombox = gtk.HBox(False, 10)
	image = gtk.Image()
        image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
        leftbox.pack_start(image, False, False, 10)
        image.show()
               
        label1 = gtk.Label("Select keyboard:")
        label1.set_line_wrap(True)
        kbdsel = gtk.combo_box_new_text()
        kbdsel.set_size_request(120, 30)
	os.system("ls /etc/X11/xkb/symbols >/tmp/kbd.txt")
	file = open('/tmp/kbd.txt')
	kbds = file.read()
	file.close()
	lines = kbds.split("\n", sys.maxint)
	for line in lines:
		if (os.path.isdir("/etc/X11/xkb/symbols/%s" % (line))):
			pass
		else:
			if (line != 'README'):
				kbdsel.append_text(line)
	kbdsel.set_active(34)
	button1 = gtk.CheckButton("Make Permanent")
	rightbox.pack_start(label1, False, False, 10)
        rightbox.pack_start(kbdsel, False, False, 10)
        rightbox.pack_start(button1, False, False, 10)
        button2 = gtk.Button("Change")
        button2.set_size_request(120, 30)
        button2.connect("clicked", key_change)
        bottombox.pack_start(button2, True, False, 10)
        button2.show()
	button3 = gtk.Button("Close")
        button3.set_size_request(120, 30)
        button3.connect("clicked", close_window)
        bottombox.pack_start(button3, True, False, 10)
        button3.show()
	button1.show()
	label1.show()
	kbdsel.show()
	mainbox.show()
	leftbox.show()
	rightbox.show()
	topbox.pack_start(leftbox, False, False, 10)
	topbox.pack_start(rightbox, False, False, 10)
	mainbox.pack_start(topbox, False, False, 10)
	mainbox.pack_start(bottombox, False, False, 10)
	leftbox.show()
	rightbox.show()
	topbox.show()
	bottombox.show()
	window.add(mainbox)
        mainbox.show()         
        window.show()
	
	return True