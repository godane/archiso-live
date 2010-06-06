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

from mkbootloader import *

class InstallGRUB:

    def close_application(self, widget, data=None):
        self.window.destroy()

    def Button1Click(self, widget, data=None):
        
	wolvix_id = file('/etc/wolvix-version').readlines()
	self.wolvix_name = wolvix_id[0].strip()
	os.system('mkdir /tmp/etc')
	grub_config(self.rootsel.get_active_text(), self.bootsel.get_active_text(), "hd", False, self.wolvix_name)
	mb = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, 
		"GRUB install complete. \nYou may now close the panel.");
        response = mb.run()
        mb.destroy()
	 
    def BootSelClick(self, widget, data=None):
        return
    
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
	self.window.set_size_request(260, 280)
	self.window.set_position(gtk.WIN_POS_CENTER)
	self.window.set_resizable(True)

	self.window.connect("destroy", self.close_application)
	self.window.set_title("Install GRUB to MBR")
	self.window.set_border_width(10)

	self.mainbox = gtk.VBox(True, 10)
	self.bottombox = gtk.HBox(False, 0)
	help = gtk.Label("\nThis utility will install GRUB \
to the Master Boot Record of your Hard Disk. \n")
	help.set_line_wrap(True)
	help.show()
	self.mainbox.pack_start(help, True, False, 0)
	label1 = gtk.Label("System boot device:")
	label1.set_line_wrap(True)
	self.mainbox.pack_start(label1, True, False, 0)
	label1.show()
	self.bootsel = gtk.combo_box_new_text()
	self.bootsel.set_size_request(100, 30)
	os.system("fdisk -l | egrep -o '/dev/[a-z]+' | uniq >/tmp/boot.txt")
	file = open('/tmp/boot.txt')
	bdisk = file.read()
	file.close()
	lines = bdisk.split("\n", sys.maxint)
	for line in lines:
		self.bootsel.append_text(line)
		self.bootsel.set_active(0)
	self.bootsel.connect("changed", self.BootSelClick, None)
	self.mainbox.pack_start(self.bootsel, True, False, 10)
	self.bootsel.show()
	label2 = gtk.Label("System root partition:")
	label2.set_line_wrap(True)
	self.mainbox.pack_start(label2, True, False, 0)
	label2.show()
	self.rootsel = gtk.combo_box_new_text()
	self.rootsel.set_size_request(100, 30)
	os.system("mount >/tmp/mount.txt")
	file = open('/tmp/mount.txt')
	mount = file.read()
	file.close()
	lines = mount.split("\n", sys.maxint)
	for line in lines:
		index = line.find("/mnt", 0, sys.maxint)  
		if (index >= 0) :
			word = line.split(None, sys.maxint)
			self.rootsel.append_text(word[2])
	self.rootsel.set_active(0)
	self.mainbox.pack_start(self.rootsel, True, False, 10)
	self.rootsel.show()
	self.button1 = gtk.Button("Go")
	self.button1.set_size_request(110, 30)
	self.button1.connect("clicked", self.Button1Click)
	self.bottombox.pack_start(self.button1, True, False, 10)
	self.button1.show()	
	self.button2 = gtk.Button("Close")
	self.button2.set_size_request(110, 30)
	self.button2.connect("clicked", self.close_application)
	self.button2.set_flags(gtk.CAN_DEFAULT)
	self.bottombox.pack_start(self.button2, True, False, 10)
	self.button2.show()
	self.mainbox.pack_start(self.bottombox, True, False, 10)
	self.bottombox.show()
	self.window.add(self.mainbox)
	self.mainbox.show()         
	self.window.show()
	