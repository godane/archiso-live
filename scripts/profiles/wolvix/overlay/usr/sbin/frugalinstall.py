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
import gtk, gobject, os, sys, thread, time
import re, os.path, shutil

from mkbootloader import *
from wolvixsave import *

class FrugalInstall:

    def list_partitions (self):
        for devs in ['/dev/hda', '/dev/hdb', '/dev/hdc', '/dev/hdd', '/dev/hde', 
            '/dev/hdf', '/dev/hdg', '/dev/hdh', '/dev/hdi', '/dev/hdj', '/dev/hdk', 
            '/dev/hdl', '/dev/hdm', '/dev/hdn', '/dev/hdo', '/dev/hdp', '/dev/sda', 
            '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg',
            '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm', 
            '/dev/sdn', '/dev/sdo', '/dev/sdp']:
            os.system("fdisk -l %s >>/tmp/devs.txt" % devs)

    def PartSelClick(self, widget, data=None):
        count = 0
        index = -1
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
	for line in file('/tmp/fdisk.txt').readlines():
             word = line.split(None, sys.maxint)
             if (word.count("Boot")): 
                 word.remove("Boot")
             if (word.count("*")): word.remove("*")
             if (word.count("Blocks")): 
                 index = word.index("Blocks")
             if (word.count(self.partsel.get_active_text())): 
                 self.size = word[index]
                 count = count+1
        index = self.size.find('+')
        if (index >= 0):
            newsize = self.size[:index]
        else:
            newsize = self.size
        self.space = (newsize)
        if (self.space > 1600000): 
             self.partitionok = True
        else: 
            self.partitionok = False
        mountpoint = "/mnt/" + self.partsel.get_active_text()[5:]
        
    def progress_update(self, widget, data):
	percent = 0.001
        while percent < 1.0:
		mountpoint = "/mnt/" + self.partsel.get_active_text()[5:]
		os.system("du -b -s %s > /tmp/df.txt" % mountpoint)
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

    def make_changes(self, widget, data=None):
        changes = WolvixSave()
	return

    def Button0Click(self, widget, data=None):
        return
    
    def Button1Click(self, widget, data=None):
        return
    
    def Button2Click(self, widget, data=None):
        dialog = gtk.FileChooserDialog("Select...", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_CANCEL)
        resp = dialog.run()
        if (resp == gtk.RESPONSE_OK):
		self.button2.set_label(dialog.get_current_folder())
		self.srcdir = dialog.get_current_folder()
        dialog.destroy()
        return
    
    def callback(self, widget, data=None):
        return
        
    def Button4Click(self, widget, data=None):
        message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "The gparted disk partition utility will now start. This utility \
will allow you to create/resize/delete partitions on your \
hard disk. As a minimum, you must have a root partition large \
enough for the Wolvix system (1.5GB). You may also want to \
have a separate home partition (~500MB) so your configuration \
and data files are not lost if you re-install Wolvix at a \
later date. You should also have a swap partition, around \
twice the size of your physical memory.\n\n\
To use gparted, right click on the partition to be changed or \
on free space to create a new partition. You may need to delete \
or resize existing partitions to make room for the new ones. For \
swap, select 'New' and then in the dialog box which opens, select \
'create primary partition' and select 'filesystem: linux-swap', \
then click add. \n\n\
If you need more than the maximum 4 primary partitions, have no \
more than 3 primary partitions, and one extended. You can then \
create multiple logical partitions within the extended one. Note \
that partitions must be unmounted before they can be deleted/resized.\n\n\
When you have finished making changes, click the green tick \
icon to apply changes, then from the menu select Gparted: refresh \
devices to see your new layout. When you are happy with the layout, \
close the utility.\n\n\
You may leave this window open as an aide-memoire until you have \
finished with the partitioner. Do not worry too much if gparted \
gives error messages - if the installer does not run properly, you \
may need to reboot Wolvix and run the installer again to register \
the new partitions with the kernel.")
        ans = os.system("gparted &")
        resp = message.run()
        message.destroy()
        self.populate(None)
        
    # Callback that starts the install process
    # ########################
    def Button5Click(self, widget, data=None):
        
	self.get_wolvix_size(self, None)
	mountpoint = "/mnt/" + self.partsel.get_active_text()[5:]
        print "Source dir = %s\nTarget dir = %s\n" %(self.srcdir, mountpoint)
	#if(self.changes.get_active()): 
	#    self.make_changes(self, None)
        if (mountpoint==self.srcdir):
            message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
                "Source location is the same as target location.\n\
Not recommended, and not allowed.")
            resp = message.run()
            message.destroy()
            return
        os.system ("umount %s" % mountpoint)				
	os.system("mkfs -t ext3 %s" % self.partsel.get_active_text())					
        print "mounting %s on %s" % (self.partsel.get_active_text(), mountpoint)
	os.system ("mkdir %s" % mountpoint)
	os.system ("mount %s %s" % (self.partsel.get_active_text(), mountpoint))				
        os.system ("mount > /tmp/mount.txt")				
        for line in open('/tmp/mount.txt').readlines():
            word = line.split(None, sys.maxint)
            if (word.count("%s" % mountpoint)):
                mounted = True;
        
	if (mounted == False):
            message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, 
                "Fatal: Unable to mount %s." % mountpoint)
            resp = message.run()
            message.destroy()
            return
	        
        self.button0.set_sensitive(False)
	self.button2.set_sensitive(False)
	self.button4.set_sensitive(False)
	self.button5.set_sensitive(False)
	self.button6.set_sensitive(False)
	self.button8.set_sensitive(False)
	self.partsel.set_sensitive(False)
	self.changes.set_sensitive(False)
	
        thread.start_new_thread(self.progress_update, (self, self.wolvix_size))
        os.system("cp -Rp %s/* %s/" % (self.srcdir, mountpoint))
        if (self.button1.get_active()):
            if self.button0.get_active():
                cdboot=True
                os.system("mkdir %s/boot/grub" % mountpoint)
                os.system("cp /usr/sbin/memdisk.bin %s/boot/grub" % mountpoint)
                os.system("cp /usr/sbin/sbootmgr.dsk %s/boot/grub" % mountpoint)
            else:
                cdboot=False;
            grub_config(mountpoint, self.partsel.get_active_text()[:8], "hd", cdboot, self.wolvix_name)
        else:
            message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "\nNo bootloader selected to write to MBR.\nYou'll need to add wolvix to your bootloader later.\n")
            resp = message.run()
            message.destroy()
        self.button0.set_sensitive(True)
	self.button2.set_sensitive(True)
	self.button4.set_sensitive(True)
	self.button5.set_sensitive(True)
	self.button6.set_sensitive(True)
	self.button8.set_sensitive(True)
	message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "Frugal Installation complete. You may now close the \
installer and reboot into the new live system if you wish.")
        resp = message.run()
        message.destroy()
    
    def Button6Click(self, widget, data=None):

        def close_help (self):
            window.destroy()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(480, 440)
        window.set_position(gtk.WIN_POS_CENTER)
        window.set_resizable(False)
        window.set_title("Wolvix LiveCD Installer Help")
        window.set_border_width(10)

        fixed = gtk.Fixed()
  
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_IN)
        sw.set_size_request(430, 360)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        textview = gtk.TextView()
        textview.set_wrap_mode(gtk.WRAP_WORD)
        textbuffer = gtk.TextBuffer()
        textbuffer.set_text("Wolvix 'poormans' (frugal) installer\n\
\n\
License:	GNU General Public license\n\
Author: 	Chris Gallienne\n\
Date:	20th September 2006\n\
\n\
Note: This script was wholly written by me, but I have lifted ideas\
from various other installer shell scripts, principally the following:\n\
\n\
DamnSmallLinux dsl-hdinstall script, which was itself a modification \
of the KNOPPIX knx-hdinstall 0.37 by Christian Perle; the knoppix\
scripts 'knoppix-installer' by Fabian Franz and 'mkboot' by Guy Maor;\
and the 'slax-installer' scripts by Thomas Matejicek. \n\
\n\
WARNING: This program is in development. Use it at your own risk! \n\n\
USAGE:\n\
The 'Frugal Install' permits you to install Wolvix in 'LiveCD mode' to a hard \
disk partition, and run it from there, in 'LiveCD mode'. The advantage of \
this is that the system runs much more quickly than from a CDROM and \
this also frees up the CDROM drive for other use if you only have one. You \
also download and use live modules from the Wolvix or Slax web sites \
using the 'uselivemod' command.\n\n\
INSTALLATION:\n\
You must perform the following steps to use this installer:\n\n\
1: Select the source from which you wish to install the LiveCD system.\
the default is '/mnt/live/mnt/hdx'. If you are running the live CD. 'hdx' \
will be your CDROM drive. If you are running a hard disk installation of \
Linux, you should select the path to a CDROM drive containing the Wolvix \
LiveCD, or a directory where a Wolvix LiveCD iso has been mounted using \
'mount -o loop xxxxxx.iso /mnt/your_dir'. \n\n\
2: Select the target partition from which your wish to run the live CD.\
This is may be any partition on your primary hard disk. The installer \
will format this partition, so be sure it has no data you want to keep! \
If you have not already prepared a partition for the Wolvix system you \
may do so by clicking on the 'Run gparted' button, and creating a partition \
using that tool. You may get some error messages from gparted, due to \
new partitions not being registered, but these may be ignored at this stage. \
After exiting the gparted utility the new partitioning scheme should be available \
within the installer. If not, close and restart the installer. \
You MAY have to reboot Wolvix before continuing, in order to register the \
changes with the kernel.\n\n\
3: Optionally, select a partition to save changes.\
This will mean that any changes you make to your live system will be saved \
and restored next time you start the live system. You will be asked if you want \
to format this partition. If you have a previously saved set of changes you wish \
to keep, answer 'no'. If you boot from CD, you will need to use the 'changes = \
/dev/hdxx' option where hdxx is your chosen partition. If you choose to use a \
bootloader this option will be set up automatically\n\n\
4: Optionally, you may choose to install a bootloader.\
If you do so, the installed live system will appear as an option next time you boot the \
system, along with any other operating systems detected by the installer. \
Alternatively, you must boot with the LiveCD in your CDROM drive, and \
at the boot prompt type: 'wolvix nocd'. The system will detect and boot your frugal \
install, and you may remove the CD from your drive. If you elect to install a \
bootloader, you also have the option to set it up to boot from CDROM. This is \
useful if your BIOS does not support CDROM booting.\n\n\
5: Click 'Start Install' and your Wolvix system will be installed in a few \
minutes, depending upon the speed of your hardware. For example, \
on my Athlon 2400+ system the frugal install process takes around 2 minutes\n\n\
6: Reboot with the Wolvix LiveCD in your CDROM drive, or using your regular boot-\
loader. If you are using the Live CD to boot, at the boot prompt type: 'wolvix nocd' \
or 'wolvix nocd changes=/dev/your_dir' if you created a 'changes' directory. The \
system will detect and boot your frugal install, and then you may remove the CD \
from your drive, if appropriate.\n\n\
7: Enjoy!\n\n")
        textview.set_buffer(textbuffer)
        textview.show()
        sw.add(textview)
        sw.show()
        fixed.put(sw, 15, 15) 
        
        button = gtk.Button("Close")
        button.set_size_request(80, 30)
        button.connect("clicked", close_help)
        button.show()
        fixed.put(button, 200, 385)
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
            index = line.find("Linux", 0, sys.maxint)
            if ((index >= 0) and (line.find("swap", 0, sys.maxint)<0) and (line.count("/dev"))):
                 word = line.split(None, sys.maxint)
                 self.partsel.append_text(word[0])
                 self.partsel.set_active(0)
                 
    def close_application(self, widget, data=None):
        self.window.destroy()

    def get_wolvix_size(self, widget, data=None):
        wolvix_id = file('/etc/wolvix-version').readlines()
	self.wolvix_name = wolvix_id[0].strip()
	os.system("du -b -s %s > /tmp/size.txt" % self.srcdir)
	line = file('/tmp/size.txt').readlines()
	words = line[0].split(None, sys.maxint)
	self.wolvix_size = float(words[0])
	os.system("rm /tmp/size.txt")	
	print "Installed size = %s\n" %self.wolvix_size
	
    def __init__(self):
        gtk.rc_parse("/etc/gtk/gtkrc.iso-8859-2")
        message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE, 
            "WARNING: This program is in development. Use it at your own \n\
risk. Installation of a live CD to hard disk is never entirely \n\
without risk - live CDs are generally not designed to be installed\n\
to HD. Having said that, this program has been tested as \n\
thoroughly as possible, without error. Continue?") 
        message.add_button(gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
        message.add_button(gtk.STOCK_NO, gtk.RESPONSE_REJECT)
        resp = message.run()
        message.destroy()
        if (resp == gtk.RESPONSE_REJECT):
            self.close_application(self, None)
        self.wolvix_size = 0.0
	self.srcdir = ""
	self.homepoint = ""
        self.partitionok = False
        self.size=""
        self.used = "0"
        self.timer = gobject
        self.space=0
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(380, 380)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_resizable(True)

        self.window.connect("destroy", self.close_application)
        self.window.set_title("Wolvix LiveCD Frugal Install")
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
        self.button2.set_size_request(120, 30)
        os.system('ls /mnt/live/mnt > /tmp/livemnt.txt')
	for line in file('/tmp/livemnt.txt').readlines():
		line = line[0:4]
		self.srcdir = '/mnt/live/mnt/' + line.replace('\n', '')
	self.button2.set_label(self.srcdir)
        self.button2.connect("clicked", self.Button2Click)
        self.button2.show()	
        label2 = gtk.Label("2:Select Target:")
        label2.set_line_wrap(True)
        self.partsel = gtk.combo_box_new_text()
        self.partsel.set_size_request(120, 30)
        label3 = gtk.Label("3:Optional: Changes:")
        label3.set_line_wrap(True)
        self.changes = gtk.CheckButton("Make WolvixSave")
        self.changes.connect("toggled", self.make_changes, "GRUB")
        self.populate(self, None)
        self.leftbox.pack_start(label1, False, False, 0)
        self.leftbox.pack_start(self.button2, False, False, 0)
        self.leftbox.pack_start(label2, False, False, 0)
        self.leftbox.pack_start(self.partsel, False, False, 0)
        self.leftbox.pack_start(label3, False, False, 0)
        self.leftbox.pack_start(self.changes, False, False, 0)
        self.partsel.connect("changed", self.PartSelClick, None)
        label1.show()
        label2.show()
        label3.show()
        self.button2.show()
        self.partsel.show()
        self.changes.show()
       
        self.topbox.pack_start(self.leftbox, True, False, 10)
        self.topbox.pack_start(self.rightbox, True, False, 10)
        self.leftbox.show()
        self.rightbox.show()
        
        self.middlebox = gtk.HBox(False, 10)
        self.bottombox = gtk.HBox(False, 10)
        self.button4 = gtk.Button("Run gparted?")
        self.button4.set_size_request(120, 30)
        self.button4.connect_object("clicked", self.Button4Click, self.window, None)
        self.button4.set_flags(gtk.CAN_DEFAULT)
        self.middlebox.pack_start(self.button4, True, False, 10)
        self.button4.show()
        self.button6 = gtk.Button("Help")
        self.button6.set_size_request(120, 30)
        self.button6.connect("clicked", self.Button6Click)
        self.middlebox.pack_start(self.button6, True, False, 10)
        self.button6.show()	
        self.button8 = gtk.Button("Close")
        self.button5 = gtk.Button("5: Start Install")
        self.button5.set_size_request(120, 30)
        self.button5.connect("clicked", self.Button5Click)
        self.bottombox.pack_start(self.button5, True, False, 10)
        self.button5.show()	
        self.button8.set_size_request(120, 30)
        self.button8.connect("clicked", self.close_application)
        self.button8.set_flags(gtk.CAN_DEFAULT)
        self.bottombox.pack_start(self.button8, True, False, 10)
        self.button8.show()

        self.upperbox = gtk.HBox(False, 10)
        self.label0 = gtk.Label("4: Use Bootloader?")
        self.label0.set_line_wrap(True)
        self.button1 = gtk.CheckButton("Install GRUB")
        self.button1.connect("toggled", self.Button1Click, "GRUB")
        self.button0 = gtk.CheckButton("CD boot option")
        self.button0.connect("toggled", self.Button0Click, "GRUB")
        self.upperbox.pack_start(self.label0, True, False, 5)
        self.upperbox.pack_start(self.button1, True, False, 5)
        self.upperbox.pack_start(self.button0, True, False, 5)
        self.label0.show()
        self.button1.show()
        self.button0.show()

        self.pbar = gtk.ProgressBar()
        self.pbar.set_size_request(260, 20)

        self.mainbox.pack_start(self.topbox, True, True, 0)
        self.topbox.show()
        self.mainbox.pack_start(self.pbar, True, False, 0)
        self.pbar.show()
        self.mainbox.pack_start(self.upperbox, True, False, 0)
        self.upperbox.show()
        self.mainbox.pack_start(self.middlebox, False, False, 5)
        self.middlebox.show()
        self.mainbox.pack_start(self.bottombox, False, False, 5)
        self.bottombox.show()
        
        self.window.add(self.mainbox)
        self.mainbox.show()         
        self.window.show()

        
