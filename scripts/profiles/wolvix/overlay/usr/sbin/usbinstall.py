#!/usr/bin/env python
#
# Program to perform frugal install of Wolvix to hard disk
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
# and the 'slax-installer' scripts by Thomas Matejicek. 

import pygtk
pygtk.require('2.0')
import gtk, gobject, os, sys, time, thread
import re, os.path, shutil

from mkbootloader import *
from wolvixsave import *

class USBInstall:

    def list_partitions (self):
        for devs in ['/dev/hda', '/dev/hdb', '/dev/hdc', '/dev/hdd', '/dev/hde', 
            '/dev/hdf', '/dev/hdg', '/dev/hdh', '/dev/hdi', '/dev/hdj', '/dev/hdk', 
            '/dev/hdl', '/dev/hdm', '/dev/hdn', '/dev/hdo', '/dev/hdp', '/dev/sda', 
            '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg',
            '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm', 
            '/dev/sdn', '/dev/sdo', '/dev/sdp']:
            os.system("fdisk -l %s >>/tmp/devs.txt" % devs)

    def changes_msg(self, widget, data=None):
	if (self.free_space > 64*1024*1024):
		self.changes.set_active(True)
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
			"Your target will have %sMB of space remaining after install.\n\
A WolvixSave file up to %sMB in size may be created." %(self.free_space/(1024*1024), 32*(int(self.free_space/(1024*1024))/32)))
		resp = message.run()
		message.destroy()
		
	else:
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
			"Your target has insufficient space for a useful WolvixSave file." )
		resp = message.run()
		message.destroy()
	return

    def get_wolvix_size(self, widget, data=None):
        wolvix_id = file('/etc/wolvix-version').readlines()
	self.wolvix_name = wolvix_id[0].strip()
	os.system("du -b -s %s > /tmp/size.txt" % self.srcdir)
	line = file('/tmp/size.txt').readlines()
	words = line[0].split(None, sys.maxint)
	self.wolvix_size = float(words[0])
	os.system("rm /tmp/size.txt")	
	print "Install requires a minimum of: %s Bytes\n" % self.wolvix_size
	
    def checkspace(self, widget, data=None):
        self.space = ""
	self.cyls = ""
	os.system("sfdisk -l %s > /tmp/size.txt" %self.partsel.get_active_text()[:8])
	for line in file('/tmp/size.txt').readlines():
		if line.count("Disk"):
			word = line.split(None, sys.maxint)
			self.cyls = word[2]
	os.system("rm /tmp/size.txt")
	os.system("sfdisk -s %s > /tmp/size.txt" %self.partsel.get_active_text()[:8])
	for line in file('/tmp/size.txt').readlines():
		word = line.split(None, sys.maxint)
		self.space = int(word[0])/1024
	print "Drive size = %sMB" %self.space
	print "Drive has = %s cyls" %self.cyls
	os.system("rm /tmp/size.txt")
	
        self.get_wolvix_size(self, None)
	print "Size of partition %s is : %d Bytes\n" % (self.partsel.get_active_text(), 1024*1024*self.space)
	if (self.wolvix_size > 1024*1024*self.space):
	    message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
                "There is not sufficient space on the target partition for Wolvix!")
            resp = message.run()
            message.destroy()
            return
	self.free_space = int(1024*1024*self.space - self.wolvix_size)
	print "Free space for wolvixsave = %d\n" %self.free_space
	adj = gtk.Adjustment(640.0, 64.0, 64*(self.free_space/(1024*1024)/64), 64.0, 5.0, 0.0)
	self.spinner.set_adjustment(adj)
	self.spinner.update()
	self.changes.set_sensitive(True)
	self.spinner.set_sensitive(True)
	
    
    def PartSelClick(self, widget, data=None):
        self.mountpoint = "/mnt/" + self.partsel.get_active_text()[5:8] + "1"
        print "Source dir = %s\nTarget dir = %s\n" %(self.srcdir, self.mountpoint)
	if (self.mountpoint==self.srcdir):
            message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
                "Source location is the same as target location.\n\
Not recommended, and not allowed.")
            resp = message.run()
            message.destroy()
            return
	self.checkspace(self, None)
	os.system('ls /mnt/live/mnt > /tmp/livemnt.txt')
	for line in file('/tmp/livemnt.txt').readlines():
		line = line[0:4]
		if line == self.partsel.get_active_text()[5:9]:
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
			"Target partition is mounted as live system. \
Cannot make filesystem here!")
			resp = message.run()
			message.destroy()
			return
	self.button5.set_sensitive(True)
	
    def make_changes(self, widget, data=None):
        changes = WolvixSave()
	return
	
    def progress_update(self, widget, data):
	percent = 0.001
        while percent < 1.0:
		os.system("du -b -s %s > /tmp/df.txt" % self.mountpoint)
		for line in file('/tmp/df.txt').readlines():
			word = line.split(None, sys.maxint)
			self.used = word[0]
		space_used = float(self.used)
		percent = 0.01+space_used/(data)
		if (percent > 1.0):
			percent = 1.0
		text = str(int(100*percent))
		text = "Copying files: " + text + "%"
		self.pbar.set_fraction(percent)
		self.pbar.set_text(text)
		while gtk.events_pending():
			gtk.main_iteration()
			
    def prep_part(self, widget, data=None):
	part = self.partsel.get_active_text()[4:8]
	print "Looking for mounted partitions in %s\n" % part 
       	os.system('mount > /tmp/mnt.txt')
        for line in file('/tmp/mnt.txt').readlines():
		word = line.split(None, sys.maxint)
		if line.count(part):
			print "Unmounting %s\n" % word[2]
			os.system("umount %s" % word[2])				
	os.system("rm /tmp/mnt.txt")
	os.system("sfdisk %s << EOF\n0,%s,0B\n;\n;\n;\nEOF\n" %(self.partsel.get_active_text()[:8], self.cyls))
	print("Running mkdosfs -F 32 %s1" %self.partsel.get_active_text()[:8])
	os.system("mkdosfs -F 32 %s1" %self.partsel.get_active_text()[:8])
	os.system("sfdisk -A1 %s" %self.partsel.get_active_text()[:8])
	message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "A single bootable partition of %sMB has been created." %self.space)
        resp = message.run()
        message.destroy()
	
    def InstallClick(self, widget, data=None):
	part = self.partsel.get_active_text()[5:]
       	required = int(self.wolvix_size)
	if (self.changes.get_active()):
		required = required + 1024*1024*self.spinner.get_value()
		print "Wolvixsave.xfs requires a minimum of: %s Bytes\n" % int(1024*1024*self.spinner.get_value())
	if (required < 1024*1024*self.space):
		print "%s has sufficient space for this install\n" %self.partsel.get_active_text()[:8]
		self.button5.set_sensitive(True)
	else:
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
                "%s does not have sufficient space for this install." %self.partsel.get_active_text()[:8])
		resp = message.run()
		message.destroy()
		return
	message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE,
                "Warning. All data on %s is about to \
to be destroyed. Continue?" %self.partsel.get_active_text()[:8])
	message.add_button(gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
        message.add_button(gtk.STOCK_NO, gtk.RESPONSE_REJECT)
        resp = message.run()
	message.destroy()
	if (resp == gtk.RESPONSE_REJECT):
		return
	self.prep_part(self, None)
	print "mounting %s1 on %s" % (self.partsel.get_active_text()[:8], self.mountpoint)
	os.system ("mkdir %s" % self.mountpoint)
	os.system ("mount %s1 %s" % (self.partsel.get_active_text()[:8], self.mountpoint))				
        os.system ("mount > /tmp/mount.txt")				
        for line in open('/tmp/mount.txt').readlines():
            word = line.split(None, sys.maxint)
            if (word.count("%s" % self.mountpoint)):
                mounted = True;
        if (mounted == False):
            message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
                "Fatal: Unable to mount %s." % self.mountpoint)
            resp = message.run()
            message.destroy()
            return
	self.partsel.set_sensitive(False)
	self.button2.set_sensitive(False) 
	self.button3.set_sensitive(False)
	self.button5.set_sensitive(False)
	self.button6.set_sensitive(False)
	self.button8.set_sensitive(False)
	thread.start_new_thread(self.progress_update, (self, self.wolvix_size))
        os.system("cp -a %s/* %s/" % (self.srcdir, self.mountpoint))
        if (self.changes.get_active()):
		os.system('touch /tmp/run')
		os.system("/usr/sbin/restart_status.py 'creating wolvixsave.xfs' & dd bs=1M count=%s if=/dev/zero of=%s/wolvixsave.xfs" %(int(self.spinner.get_value()), self.mountpoint))
		os.system('rm /tmp/run')
		os.system('touch /tmp/run')
		os.system("/usr/sbin/restart_status.py 'formatting wolvixsave.xfs' & mkfs -t xfs -f %s/wolvixsave.xfs"% self.mountpoint)				
		os.system('rm /tmp/run')			
		os.system ("umount %s" % self.mountpoint)				
	        
	if (self.button3.get_active()):
		os.system('syslinux -s %s1' % self.partsel.get_active_text()[:8])	
	else:
		os.system('syslinux %s1' % self.partsel.get_active_text()[:8])	
	self.partsel.set_sensitive(True)
	self.button2.set_sensitive(True)
	self.button3.set_sensitive(True)
	self.button5.set_sensitive(True)
	self.button6.set_sensitive(True)
	self.button8.set_sensitive(True)
	message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "USB Installation complete. You may now close the \
installer and reboot into the new live system if you wish.")
        resp = message.run()
        message.destroy()
    
    def HelpClick(self, widget, data=None):

        def close_help (self):
            window.destroy()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(520, 580)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_resizable(False)
        window.set_title("Wolvix LiveCD Installer Help")
        window.set_border_width(10)

        fixed = gtk.Fixed()
  
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.set_size_request(480, 480)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textbuffer = gtk.TextBuffer()
        textbuffer.set_text("Wolvix USB installer\n\
\n\
License:			GNU General Public license\n\
Author: 			Chris Gallienne (oithona)\n\
Date:			30th September 2006\n\
Last revision:   	6th January 2009\n\
\n\
WARNING: This program is in development. Use it at your own risk! \n\n\
USAGE:\n\
The USB Installer permits you to install Wolvix in 'Live mode' to a USB \
flash disk, and run it from there, in 'LiveCD mode'. Check that your PC \
is capable of booting from a USB drive before you begin!\n\n\
INSTALLATION:\n\
You must perform the following steps to use this installer:\n\n\
1: Select the source from which you wish to install the USB Live system. \
The default is '/mnt/live/mnt/hdx'. If you are running the live CD, 'hdx' \
will be your CDROM drive. If you are running a hard disk installation of \
Linux, you should select the path to a CDROM drive containing the Wolvix \
LiveCD, or a directory where a Wolvix LiveCD iso has been mounted using \
'mount -o loop xxxxxx.iso /mnt/your_dir'. \n\n\
2: Select the target (USB) device partition to which you wish to install Wolvix. \
This is likely to be something like '/dev/sda1'. The installer will format \
this partition using a FAT32 filesystem, so be sure it has no data you want \
to keep! \n\n\
3: Optionally, elect to create a persistent storage area where your changes \
will be saved and will be available next time you boot the usb system. The \
storage area is a file called wolvixsave.xfs created in the root of your target \
partition. Choose its size, between 64MB and 2048MB or the size of free space \
on your drive, whichever is the smaller, in increments of 64MB.\n\n\
4: Option: Some older & 'buggy' BIOSes fail syslinux installation. The slow \
boot option can fix this issue. If your USB installation fails to boot, \
you can try it again with the slow boot option.\n\n\
5:  Click 'Start Install' and your Wolvix system will be installed in a few \
minutes, depending upon the speed of your hardware. \n\n\
Note: If your computer is unable to boot from USB, you can use a floppy boot \
disk which uses DOS USB drivers. There are several variations available as \
downloadable disk images. One such is called 'wolvix_usb_cd_boot.img' and \
is available at wolvix.org.\n\n")
        textview.set_buffer(textbuffer)
        textview.show()
        sw.add(textview)
        sw.show()
        fixed.put(sw, 15, 15) 
        
        button = gtk.Button("Close")
        button.set_size_request(80, 30)
        button.connect("clicked", close_help)
        button.show()
        fixed.put(button, 220, 525)
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
            if line.count("/dev/sd", 0, sys.maxint) and line.count("Disk"):
                 word = line.split(None, sys.maxint)
                 self.partsel.append_text("%s %s%s" %(word[1][:8], word[2], word[3]))
                 #self.partsel.set_active(0)
                 
    def close_application(self, widget, data=None):
        self.window.destroy()

    def SourceClick(self, widget, data=None):
	dialog = gtk.FileChooserDialog("Select...", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_CANCEL)
        resp = dialog.run()
        if (resp == gtk.RESPONSE_OK):
		self.button2.set_label(dialog.get_current_folder())
		self.srcdir = dialog.get_current_folder()
        dialog.destroy()
        self.get_wolvix_size(self, None)
	return
    
    def __init__(self):
        gtk.rc_parse("/etc/gtk/gtkrc.iso-8859-2")
        self.wolvix_size = 0.0
	self.srcdir = ""
	self.partitionok = False
        self.size=""
        self.used = "0"
        self.timer = gobject
        self.space=0
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window.set_size_request(380, 380)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_resizable(True)

        self.window.connect("destroy", self.close_application)
        self.window.set_title("Wolvix USB Install")
        self.window.set_border_width(10)

        self.mainbox = gtk.VBox(False, 10)
        self.topbox = gtk.HBox(False, 10)
        self.leftbox = gtk.VBox(False, 10)
        self.rightbox = gtk.VBox(False, 10)
        image = gtk.Image()
        image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
        self.rightbox.pack_start(image, False, False, 10)
        image.show()
               
        label1 = gtk.Label("1: Select source:")
        label1.set_line_wrap(True)
        self.button2 = gtk.Button("Select source")
        self.button2.set_size_request(140, 30)
        os.system('ls /mnt/live/mnt > /tmp/livemnt.txt')
	for line in file('/tmp/livemnt.txt').readlines():
		line = line[0:4]
		self.srcdir = '/mnt/live/mnt/' + line.replace('\n', '')
	self.button2.set_label(self.srcdir)
        self.button2.connect("clicked", self.SourceClick)
        self.button2.show()	
        label2 = gtk.Label("2:Select Target:")
        label2.set_line_wrap(True)
        self.partsel = gtk.combo_box_new_text()
        self.partsel.set_size_request(140, 30)
        self.populate(self, None)
        label3 = gtk.Label("3:Optional - Save Changes:")
        label3.set_line_wrap(True)
        self.changes = gtk.CheckButton("Make WolvixSave")
        self.change_box = gtk.HBox(False, 10)
        label4 = gtk.Label("Size in MB:")
        adj = gtk.Adjustment(640.0, 64.0, 2048.0, 1.0, 5.0, 0.0)
	self.spinner = gtk.SpinButton(adj, 0, 0)
	self.spinner.set_wrap(True)
	self.label5 = gtk.Label("4: Optional - use slow boot")
	self.button3 = gtk.CheckButton("Slow Boot")
	self.changes.set_sensitive(False)
	self.changes.connect("pressed", self.changes_msg, None)
	self.spinner.set_sensitive(False)
	self.change_box.pack_start(label4, True, False, 0)
        self.change_box.pack_start(self.spinner, False, True, 0)
	label4.show()
	self.spinner.show()
	self.leftbox.pack_start(label1, True, False, 0)
        self.leftbox.pack_start(self.button2, True, False, 0)
        self.leftbox.pack_start(label2, True, False, 0)
        self.leftbox.pack_start(self.partsel, True, False, 0)
        self.leftbox.pack_start(label3, True, False, 0)
        self.leftbox.pack_start(self.changes, True, False, 0)
        self.leftbox.pack_start(self.change_box, True, False, 0)
        self.partsel.connect("changed", self.PartSelClick, None)
        self.leftbox.pack_start(self.label5, True, False, 0)
        self.leftbox.pack_start(self.button3, True, False, 0)
        label1.show()
        label2.show()
        self.button2.show()
        self.partsel.show()
        label3.show()
        self.changes.show()
        self.change_box.show()
        self.button3.show()
        self.label5.show()
        self.topbox.pack_start(self.leftbox, True, False, 10)
        self.topbox.pack_start(self.rightbox, True, False, 10)
        self.leftbox.show()
        self.rightbox.show()
        
        self.bottombox = gtk.HBox(False, 10)
        self.button5 = gtk.Button("5: Start Install")
        self.button5.set_size_request(120, 30)
        self.button5.connect("clicked", self.InstallClick)
	self.button5.set_sensitive(False)
        self.bottombox.pack_start(self.button5, True, False, 10)
        self.button5.show()	
        self.button6 = gtk.Button("Help")
        self.button6.set_size_request(120, 30)
        self.button6.connect("clicked", self.HelpClick)
        self.bottombox.pack_start(self.button6, True, False, 10)
        self.button6.show()	
        self.button8 = gtk.Button("Close")
        self.button8.set_size_request(120, 30)
        self.button8.connect("clicked", self.close_application)
        self.button8.set_flags(gtk.CAN_DEFAULT)
        self.bottombox.pack_start(self.button8, True, False, 10)
        self.button8.show()

        self.pbar = gtk.ProgressBar()
        self.pbar.set_size_request(200, 20)

        self.mainbox.pack_start(self.topbox, True, True, 0)
        self.topbox.show()
        self.mainbox.pack_start(self.pbar, False, False, 10)
        self.pbar.show()
        self.mainbox.pack_start(self.bottombox, False, False, 5)
        self.bottombox.show()
        
        self.window.add(self.mainbox)
        self.mainbox.show()         
        self.window.show()

        
