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

class WolvixSave:

    def list_partitions (self):
        for devs in ['/dev/hda', '/dev/hdb', '/dev/hdc', '/dev/hdd', '/dev/hde', 
            '/dev/hdf', '/dev/hdg', '/dev/hdh', '/dev/hdi', '/dev/hdj', '/dev/hdk', 
            '/dev/hdl', '/dev/hdm', '/dev/hdn', '/dev/hdo', '/dev/hdp', '/dev/sda', 
            '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg',
            '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm', 
            '/dev/sdn', '/dev/sdo', '/dev/sdp']:
            os.system("fdisk -l %s >>/tmp/devs.txt" % devs)

    def PartSelClick(self, widget, data=None):
        os.system("df > /tmp/df.txt")
	file = open('/tmp/df.txt')
	df = file.read()
	file.close()
	count = 0
	index = -1
	self.size = "0"
	found = False
	lines = df.split("\n", sys.maxint)
	for line in lines:
		word = line.split(None, sys.maxint)
		if (word.count("Available")):
			index = word.index("Available")
			print "Found Avail at index %s" %index
		if (word.count(self.partsel.get_active_text())):
			self.size = word[index]
			print "size = %s\n" %self.size
			count = count+1
			found = True
	if (found == False):
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                    "%s not mounted - cannot estimate free space." %self.partsel.get_active_text())
                resp = message.run()
                message.destroy()
	        return
	self.newsize = int(self.size)
	print "Partition free space = %s" %self.newsize
	return
        
    # Callback that starts the install process
    # ########################
    def Button5Click(self, widget, data=None):
        
        self.newsize=0
	self.PartSelClick(self, None)
	filesize = 	self.file_size.get_text()
	if (int(filesize)*1024.0 > self.newsize*1.0):
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                    "Not enough space for WolvixSave file here.")
                resp = message.run()
                message.destroy()
	        return
	mountpoint = "/mnt/" + self.partsel.get_active_text()[5:]
	os.system("mount %s" %mountpoint)
	os.system("mount > /tmp/mount.txt")
	for line in file('/tmp/mount.txt').readlines():
             word = line.split(None, sys.maxint)
             if (word.count(mountpoint)): 
                 if (word.count("ntfs") and word.count("(ro,noatime)")): 
		    message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_YES_NO, 
                    "NTFS filesystem is read-only! Do you wish enable write support?")
                    resp = message.run()
                    message.destroy()
		    if (resp == gtk.RESPONSE_NO):
		        message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
                            "Unable to create WolvixSave file here.")
                        resp = message.run()
                        message.destroy()
		        return
		    else:
			os.system("umount %s" %mountpoint)
			sleep(2)
	                os.system("ntfs-3g %s %s" %(self.partsel.get_active_text(), mountpoint))
                        
        os.system('touch /tmp/run')
	os.system("/usr/sbin/restart_status.py 'creating wolvixsave.xfs...' & dd bs=1M count=%s if=/dev/zero of=%s/wolvixsave.xfs" % (filesize, mountpoint))
	os.system('rm /tmp/run')
	os.system('touch /tmp/run')
	os.system("/usr/sbin/restart_status.py 'formatting wolvixsave.xfs' & mkfs -t xfs -f %s/wolvixsave.xfs"% mountpoint)				
        os.system('rm /tmp/run')
	message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "WolvixSave File created. If you are making a frugal install \
you may now continue with 'Start Install'. Else, you may now close the \
dialog and reboot with the new file active if you wish.")
        resp = message.run()
        message.destroy()
	self.close_wolvixsave(self, None)
    
    def Button6Click(self, widget, data=None):

        def close_help (self):
            window.destroy()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(480, 360)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_resizable(False)
        window.set_title("Persistent WolvixSave File Help")
        window.set_border_width(10)

        fixed = gtk.Fixed()
  
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.set_size_request(430, 260)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textbuffer = gtk.TextBuffer()
        textbuffer.set_text("Utility to create a persistent WolvixSave file\n\
\n\
License:	GNU General Public license\n\
Author: 	Chris Gallienne\n\
Date:	4th June 2007\n\
\n\
\n\
WARNING: This program is in development. Use it at your own risk! \n\n\
USAGE:\n\
This utility will allow you to create a wolvixsave.xfs file \
in the root directory of any partition you select. This \
file is used to preserve all changes you make to your live \
system, and all your personal data. The file will be detected \
and used automatically by a Wolvix live system (CD, USB, Frugal) \
on the next reboot.\n\n")
        textview.set_buffer(textbuffer)
        textview.show()
        sw.add(textview)
        sw.show()
        fixed.put(sw, 15, 15) 
        
        button = gtk.Button("Close")
        button.set_size_request(80, 30)
        button.connect("clicked", close_help)
        button.show()
        fixed.put(button, 200, 300)
        fixed.show()
        window.add(fixed)

        window.show()
        
    def populate(self, widget, data=None):
        os.system("fdisk -l >/tmp/fdisk.txt")
        file = open('/tmp/fdisk.txt')
        fdisk = file.read()
        file.close()
        lines = fdisk.split("\n", sys.maxint)
        for line in lines:
            index = line.find("/dev/", 0, sys.maxint)
            if ((index >= 0) and (line.find("swap", 0, sys.maxint)<0) and 
		    (line.find("Disk", 0, sys.maxint)<0)):
                 word = line.split(None, sys.maxint)
                 self.partsel.append_text(word[0])
                 self.partsel.set_active(0)
                 
    def close_wolvixsave(self, widget, data=None):
        self.wswindow.destroy()

    def __init__(self):
        gtk.rc_parse("/etc/gtk/gtkrc.iso-8859-2")
        self.srcdir = ""
	self.homepoint = ""
        self.partitionok = False
        self.size=""
        self.used = "0"
        self.timer = gobject
        self.space=0
        self.wswindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.wswindow.set_position(gtk.WIN_POS_CENTER)
        self.wswindow.set_resizable(True)

        self.wswindow.connect("destroy", self.close_wolvixsave)
        self.wswindow.set_title("Create Persistent WolvixSave File")
        self.wswindow.set_border_width(10)

        self.mainbox = gtk.VBox(False, 10)
        self.topbox = gtk.HBox(False, 10)
        self.leftbox = gtk.VBox(False, 10)
        self.rightbox = gtk.VBox(False, 10)
        image = gtk.Image()
        image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
        self.rightbox.pack_start(image, False, False, 10)
        image.show()
               
        label1 = gtk.Label("1:Select Partition:")
        label1.set_line_wrap(True)
        self.partsel = gtk.combo_box_new_text()
        self.partsel.set_size_request(120, 30)
        self.populate(self, None)
	label3 = gtk.Label("2:File Size (MB):")
        label3.set_line_wrap(True)
        self.file_size = gtk.Entry(15)
	self.file_size.set_size_request(120, 25)
        self.leftbox.pack_start(label1, False, False, 5)
        self.leftbox.pack_start(self.partsel, False, False, 0)
        self.leftbox.pack_start(label3, False, False, 5)
        self.leftbox.pack_start(self.file_size, False, False, 0)
        self.partsel.connect("changed", self.PartSelClick, None)
        label1.show()
        label3.show()
	self.file_size.show()
        self.partsel.show()
        
        self.topbox.pack_start(self.leftbox, True, False, 10)
        self.topbox.pack_start(self.rightbox, True, False, 10)
        self.leftbox.show()
        self.rightbox.show()
        
        self.bottombox = gtk.HBox(False, 10)
        self.button5 = gtk.Button("Create")
        self.button5.set_size_request(120, 30)
        self.button5.connect("clicked", self.Button5Click)
        self.bottombox.pack_start(self.button5, True, False, 10)
        self.button5.show()	
        self.button6 = gtk.Button("Help")
        self.button6.set_size_request(120, 30)
        self.button6.connect("clicked", self.Button6Click)
        self.bottombox.pack_start(self.button6, True, False, 10)
        self.button6.show()	
        self.button8 = gtk.Button("Cancel")
        self.button8.set_size_request(120, 30)
        self.button8.connect("clicked", self.close_wolvixsave)
        self.button8.set_flags(gtk.CAN_DEFAULT)
        self.bottombox.pack_start(self.button8, True, False, 10)
        self.button8.show()

        self.hseparator = gtk.HSeparator()
        
        self.mainbox.pack_start(self.topbox, True, True, 0)
        self.topbox.show()
        self.mainbox.pack_start(self.hseparator, True, False, 0)
        self.hseparator.show()
        self.mainbox.pack_start(self.bottombox, False, False, 5)
        self.bottombox.show()
        
        self.wswindow.add(self.mainbox)
        self.mainbox.show()         
        self.wswindow.show()

        