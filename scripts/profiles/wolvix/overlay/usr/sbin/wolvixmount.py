#!/usr/bin/env python
#
# Program to set up wolvixsave.xfs file to allow persistence
#
# License:	GNU General Public license
# Author: 	Chris Gallienne
#
# 

import pygtk
pygtk.require('2.0')
import gtk, gobject, os, sys, thread, time
import re, os.path, shutil

class WolvixMount:

    def list_partitions (self):
        for devs in ['/dev/hda', '/dev/hdb', '/dev/hdc', '/dev/hdd', '/dev/hde', 
            '/dev/hdf', '/dev/hdg', '/dev/hdh', '/dev/hdi', '/dev/hdj', '/dev/hdk', 
            '/dev/hdl', '/dev/hdm', '/dev/hdn', '/dev/hdo', '/dev/hdp', '/dev/sda', 
            '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg',
            '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm', 
            '/dev/sdn', '/dev/sdo', '/dev/sdp']:
            os.system("fdisk -l %s >>/tmp/devs.txt" % devs)
        
    def get_mount(self, widget, data=None):
	index = self.buttons.index(widget)
	os.system("mount -l >/tmp/mount.txt")
        file = open('/tmp/mount.txt')
        mount = file.read()
        file.close()
        lines = mount.split("\n", sys.maxint)
        for line in lines:
	    if (line.find(widget.get_label(), 0, sys.maxint)>=0):
		word = line.split(None, sys.maxint)
                self.entries[index].set_text("Mounted on %s" %word[2])
		widget.set_relief(gtk.RELIEF_NORMAL)
		return True
	return False
	
    def mount(self, widget, data=None):
	index = self.buttons.index(widget)
	if (self.type[index].count("NTFS")):
		os.system("ntfs-3g %s %s -o force\n" %(widget.get_label(), self.mountpoint))
	else:
		os.system("mount %s %s\n" %(widget.get_label(), self.mountpoint))
	mounted = self.get_mount(widget, None)
	if mounted:
		self.entries[index].set_text("Mounted on %s" % self.mountpoint)
		widget.set_relief(gtk.RELIEF_NORMAL)
	else:
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
			"Unable to mount %s!" %widget.get_label())
		resp = message.run()
		message.destroy()
	return
	
    def unmount(self, widget, data=None):
	os.system("umount %s\n" % self.mountpoint)
	index = self.buttons.index(widget)
	unmounted = not(self.get_mount(widget, None))
	if unmounted:
		self.entries[index].set_text("Not Mounted")
		widget.set_relief(gtk.RELIEF_NONE)
	else:
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
			"Unable to unmount %s!" %widget.get_label())
		resp = message.run()
		message.destroy()
	return
	
    def mount_click(self, widget, data=None):
	mounted = False;
	found = False
	for line in file('/etc/fstab').readlines():
            index = line.find(widget.get_label(), 0, sys.maxint)
            if (index >= 0):
		word = line.split(None, sys.maxint)
                self.mountpoint = word[1] + " "
		found = True
	if (found == False):
		self.mountpoint = "/mnt/" + widget.get_label()[5:] + " "
	if not os.path.isdir(self.mountpoint.strip()): os.makedirs(self.mountpoint.strip())
	os.system("mount > /tmp/mount.txt")
	for line in file('/tmp/mount.txt').readlines():
		index = line.find(self.mountpoint)
		if (index>=0):
			mounted = True
	if mounted:
		self.unmount(widget, None)
	else:
		self.mount(widget, None)   
	return
	
    def renew_mountpoints(self, widget, data=None):
	children = self.mainbox.get_children()
	for child in children:
		self.mainbox.remove(child)
	self.wswindow.remove(self.mainbox)
	self.create_mountpoints(self, None)
	
    def create_mountpoints(self, widget, data=None):
	self.mainbox = gtk.VBox(False, 10)

	self.mainbox.pack_start(self.topbox, True, True, 0)
        self.topbox.show()
        self.mainbox.pack_start(self.hseparator1, True, False, 0)
        self.hseparator1.show()
	
	self.middlebox=gtk.HBox(False, 10)
	self.midleftbox = gtk.VBox(False, 10)
        self.midcentrebox = gtk.VBox(False, 10)
        self.midrightbox = gtk.VBox(False, 10)
        self.populate(self, None)
	self.middlebox.pack_start(self.midleftbox, True, False, 0)
	self.middlebox.pack_start(self.midcentrebox, True, False, 0)
	self.middlebox.pack_start(self.midrightbox, True, False, 0)
	self.midleftbox.show()
	self.midcentrebox.show()
	self.midrightbox.show()
	self.mainbox.pack_start(self.middlebox, False, False, 5)
        self.middlebox.show()
        
	self.mainbox.pack_start(self.hseparator2, True, False, 0)
        self.hseparator2.show()
	self.mainbox.pack_start(self.bottombox, False, False, 5)
        self.bottombox.show()
        
        self.wswindow.add(self.mainbox)
        self.mainbox.show()         

    def populate(self, widget, data=None):
        self.buttons = []
	self.entries = []
	self.type=[]
	os.system("fdisk -l >/tmp/fdisk.txt")
        for line in file('/tmp/fdisk.txt').readlines():
            index = line.find("/dev/", 0, sys.maxint)
            if ((index >= 0) and (line.find("swap", 0, sys.maxint)<0) and 
		    (line.find("Disk", 0, sys.maxint)<0) and (line.find("Extended", 0, sys.maxint)<0)):
                word = line.split(None, sys.maxint)
                self.mountbutton = gtk.Button(word[0]+" ")
		self.mountbutton.set_size_request(120, 30)
		self.mountbutton.set_relief(gtk.RELIEF_NONE)
		self.mountbutton.connect("clicked", self.mount_click)
		self.mountbutton.set_flags(gtk.CAN_DEFAULT)
		self.buttons.append(self.mountbutton)
		self.midleftbox.pack_start(self.mountbutton, True, False, 0)
		if (word[1].count('*')):
			self.type.append(word[6])
			label=gtk.Label(word[6])
		else:
			self.type.append(word[5])
			label=gtk.Label(word[5])
		self.midcentrebox.pack_start(label, True, False, 0)		
		label.show()
		self.mountentry = gtk.Entry()
		self.mountentry.set_text("Not Mounted")
		self.entries.append(self.mountentry)
		self.midrightbox.pack_start(self.mountentry, True, False, 0)
		self.mountbutton.show()
		self.mountentry.show()
		self.get_mount(self.mountbutton, None)
        os.system("cat /proc/sys/dev/cdrom/info > /tmp/cdrom.txt")
	for line in file('/tmp/cdrom.txt').readlines():
		index = line.find("name:", 0, sys.maxint)
		if (index>=0):
			word = line.split(None, sys.maxint)
			self.mountbutton = gtk.Button("/dev/" + word[2] +" ")
			self.mountbutton.set_size_request(120, 30)
			self.mountbutton.set_relief(gtk.RELIEF_NONE)
			self.mountbutton.connect("clicked", self.mount_click)
			self.mountbutton.set_flags(gtk.CAN_DEFAULT)
			self.buttons.append(self.mountbutton)
			self.midleftbox.pack_start(self.mountbutton, True, False, 0)
			self.type.append("cdrom")
			label=gtk.Label("cdrom")
			self.midcentrebox.pack_start(label, True, False, 0)		
			label.show()
			self.mountentry = gtk.Entry()
			self.mountentry.set_text("Not Mounted")
			self.entries.append(self.mountentry)
			self.midrightbox.pack_start(self.mountentry, True, False, 0)
			self.mountbutton.show()
			self.mountentry.show()
			self.get_mount(self.mountbutton, None)
	os.system("ls /sys/block > /tmp/block.txt")
	for line in file('/tmp/block.txt').readlines():
		index = line.find("fd", 0, sys.maxint)
		if (index>=0):
			word = line.split(None, sys.maxint)
			self.mountbutton = gtk.Button("/dev/" + word[0] +" ")
			self.mountbutton.set_size_request(120, 30)
			self.mountbutton.set_relief(gtk.RELIEF_NONE)
			self.mountbutton.connect("clicked", self.mount_click)
			self.mountbutton.set_flags(gtk.CAN_DEFAULT)
			self.buttons.append(self.mountbutton)
			self.midleftbox.pack_start(self.mountbutton, True, False, 0)
			self.type.append("floppy")
			label=gtk.Label("floppy")
			self.midcentrebox.pack_start(label, True, False, 0)		
			label.show()
			self.mountentry = gtk.Entry()
			self.mountentry.set_text("Not Mounted")
			self.entries.append(self.mountentry)
			self.midrightbox.pack_start(self.mountentry, True, False, 0)
			self.mountbutton.show()
			self.mountentry.show()
			self.get_mount(self.mountbutton, None)

    def close_wolvixmount(self, widget, data=None):
        self.wswindow.destroy()

    def __init__(self):
        self.wswindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.wswindow.set_position(gtk.WIN_POS_CENTER)
        self.wswindow.set_resizable(True)

        self.wswindow.connect("destroy", self.close_wolvixmount)
        self.wswindow.set_title("Wolvix device mount/unmount")
        self.wswindow.set_border_width(10)

        self.topbox = gtk.HBox(False, 10)
        self.leftbox = gtk.VBox(False, 10)
        self.rightbox = gtk.VBox(False, 10)
        label = gtk.Label("Wolvix mount utility:\n\
  All detected storage devices are listed \n\
  below. Click button to mount/unmount.")
        self.rightbox.pack_start(label, False, False, 10)
	label.show()
	image = gtk.Image()
        image.set_from_file("/usr/share/icons/Tango/scalable/devices/drive-mount.svg")
        self.leftbox.pack_start(image, False, False, 10)
        image.show()
               
        self.topbox.pack_start(self.leftbox, True, False, 10)
        self.topbox.pack_start(self.rightbox, True, False, 10)
        self.leftbox.show()
        self.rightbox.show()
        
	self.bottombox=gtk.HBox(False, 10)
	self.button7 = gtk.Button("Refresh")
        self.button7.set_size_request(120, 30)
        self.button7.connect("clicked", self.renew_mountpoints)
        self.button7.set_flags(gtk.CAN_DEFAULT)
        self.bottombox.pack_start(self.button7, True, False, 10)
        self.button7.show()
	self.button8 = gtk.Button("Close")
        self.button8.set_size_request(120, 30)
        self.button8.connect("clicked", self.close_wolvixmount)
        self.button8.set_flags(gtk.CAN_DEFAULT)
        self.bottombox.pack_start(self.button8, True, False, 10)
        self.button8.show()

        self.hseparator1 = gtk.HSeparator()
        self.hseparator2 = gtk.HSeparator()
        
        self.create_mountpoints(self, None)
	self.wswindow.show()

        