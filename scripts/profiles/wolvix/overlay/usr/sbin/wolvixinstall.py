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
# and the 'slax-installer' scripts by Thomas Matejicek.
#

import pygtk
pygtk.require('2.0')
import gtk, gobject, os, sys, thread, time

from mkbootloader import *
from restart_status import *

class WolvixInstall:

	def TextBufferChange(self, widget, data=None):
		self.textview.scroll_to_iter(self.textbuffer.get_end_iter(), 0.1, True, 0.5, 0.5)

	def BootSelClick(self, widget, data=None):
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s selected for bootloader.\n" % (self.bootsel.get_active_text()))

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
		print "Thread exit!"

	def HomeSelClick(self, widget, data=None):
		if (self.homesel.get_active_text() != "None"):
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s will be used for /home\n" % (self.homesel.get_active_text()))
		else:
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "No separate home partition selected.\n")
		self.TextBufferChange(self, None)

	def SwapSelClick(self, widget, data=None):
		if (self.swapsel.get_active_text() != ""):
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s will be used for swap.\n" % (self.swapsel.get_active_text()))
		else:
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "No swap partition selected!\n")
		self.TextBufferChange(self, None)

	def FSSelClick(self, widget, data=None):
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "The %s filesystem will be used for linux partitions.\n" % (self.fssel.get_active_text()))
		self.TextBufferChange(self, None)

	def PartSelClick(self, widget, data=None):
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s selected for root partition.\n" % (self.partsel.get_active_text()))
		self.TextBufferChange(self, None)
		file = open('/tmp/fdisk.txt')
		fdisk = file.read()
		file.close()
		count = 0
		index = -1
		lines = fdisk.split("\n", sys.maxint)
		for line in lines:
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
		self.space = int(newsize)
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Size of partition %s is : " % (self.partsel.get_active_text()))
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "%d kBytes\n" % (self.space))
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Wolvix requires a minimum of: %s kBytes\n" % int(self.wolvix_size/1024))
		self.TextBufferChange(self, None)
		self.TextBufferChange(self, None)
		if (self.space > self.wolvix_size/1024):
			self.partitionok = True
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s has sufficient space for Wolvix\n" % (self.partsel.get_active_text()))
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "WARNING: All existing data on %s will be destroyed.\n" % (self.partsel.get_active_text()))
		else:
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s has insufficient space for Wolvix\n" % (self.partsel.get_active_text()))
			self.partitionok = False
		mountpoint = "/mnt/" + self.partsel.get_active_text()[5:]
		self.TextBufferChange(self, None)

	def Button2Click(self, widget, data=None):
		if (self.button2.get_active()):
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "GRUB is to be installed to MBR.\n")
		else:
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "No bootloader is to be installed.\n")
		self.TextBufferChange(self, None)

	def Button3Click(self, widget, data):
		if (self.button3.get_active()):
			self.button7.set_active(False)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s.\n" % data)
		self.TextBufferChange(self, None)

	def Button7Click(self, widget, data):
		if (self.button7.get_active()):
			self.button3.set_active(False)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s.\n" % data)
		self.TextBufferChange(self, None)

	def callback(self, widget, data=None):
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "%s was toggled %s\n" % (data, ("OFF", "ON")[widget.get_active()]))
		self.TextBufferChange(self, None)

	def Button4Click(self, widget, data=None):
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Running gparted disk partitioner\n")
		self.TextBufferChange(self, None)
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
Click 'OK' to continue. This window will remain open as a guide \
until you have finished with the partitioner. Do not worry too much \
if gparted gives error messages - if the installer does not run \
properly, you may need to reboot Wolvix and run the installer again \
to register the new partitions with the kernel.")
		resp = message.run()
		ans = os.system("gparted")
		message.destroy()
		self.renew_mountpoints(self, None)
		
	def enable_gui(self, widget, mountpoint):
		line_ask = gtk.Dialog("Startup with GUI?", None, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		line_ask.set_size_request(200, 240)
		line_ask.set_position(gtk.WIN_POS_CENTER)
		help = gtk.Label("\nBoot your installed Wolvix system to the command line, or to a GUI")
		help.set_line_wrap(True)
		help.show()
		line_ask.vbox.pack_start(help, True, False, 20)
		select1 = gtk.RadioButton(None, "Command Line", False)
		select1.show()
		line_ask.vbox.pack_start(select1, True, False, 10)
		select2 = gtk.RadioButton(select1, "GUI Login prompt", False)
		select2.show()
		line_ask.vbox.pack_start(select2, True, False, 10)
		response = line_ask.run()
		line_ask.destroy()
		file = open('%s/etc/inittab' % mountpoint)
		inittab = file.read()
		file.close()
		self.text = ""
		self.found = False
		os.unlink("%s/etc/inittab" % mountpoint)
		file = open("%s/etc/inittab" % mountpoint, 'w')
		lines = inittab.split("\n", sys.maxint)
		for line in lines:
			line = line + "\n"
			if (line.count("# Default runlevel. (Do not set to 0 or 6)")):
				self.found = True
				file.write(line)
				if (select1.get_active()):
					newline = "id:3:initdefault:\n"
					self.text = "Wolvix system will boot to CLI login" 
				else:
					newline = "id:4:initdefault:\n"
					self.text = "Wolvix system will boot to GUI login" 
				file.write(newline)
			elif (self.found):
				self.found = False
			else:	
				file.write(line)
		file.close()
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, self.text) 
		resp = message.run()
		message.destroy()
		return True
	
	# Callback that toggles the text display within the progress
	# bar trough
	def Button5Click(self, widget, data=None):
		if (self.swapsel.get_active_text()=="None"):
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
			"You have not selected a swap partition. While Wolvix will \
run without one, this is not recommended. You may continue, \
or go back to main window and run partitioner. Continue? (Y/N)")
			resp = message.run()
			message.destroy()
			if (self.fs== gtk.RESPONSE_NO):
				return

		if (self.homesel.get_active_text()!="None"):
			self.homepoint = "/mnt/" + self.homesel.get_active_text()[5:]
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
			"You have selected a separate partition for your /home directory.\n\
If this is a new partition it will need formatting - all data will \
be lost! If this is a previously-used /home partition you will already \
have a filesystem. You will not want to format it in this case.\n\
Do you want to format the /home partition?")
			resp = message.run()
			message.destroy()
			if (resp == gtk.RESPONSE_YES):
				self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nOK, formatting %s\n" % self.homesel.get_active_text())
				self.TextBufferChange(self, None)
				self.textbuffer.insert(self.textbuffer.get_end_iter(), "Unmounting %s\n" % self.homesel.get_active_text())
				os.system ("umount %s" % self.homesel.get_active_text())
				self.textbuffer.insert(self.textbuffer.get_end_iter(), "Making %s filesystem on %s\n" %  (self.fs, self.homesel.get_active_text()))
				os.system("mkfs -t %s %s" % (self.fs, self.homesel.get_active_text()))
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "Making mount point for %s\n" %  self.homesel.get_active_text())
			os.system("mkdir %s" % self.homepoint)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "Mounting %s " % self.homesel.get_active_text())
			self.TextBufferChange(self, None)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "on %s\n" % self.homepoint)
			os.system ("mount %s %s" % (self.homesel.get_active_text(), self.homepoint))
			self.TextBufferChange(self, None)
			os.system ("mount > /tmp/mount.txt")
			file = open('/tmp/mount.txt')
			mount = file.read()
			file.close()
			mounted = False;
			lines = mount.split("\n", sys.maxint)
			for line in lines:
				word = line.split(None, sys.maxint)
				if (word.count("%s" % self.homepoint)):
					mounted = True;
			if (mounted == False):
				message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Fatal: Unable to mount %s." % self.homepoint)
				resp = message.run()
				message.destroy()
				self.textbuffer.insert(self.textbuffer.get_end_iter(), "Failed to mount %s\n" %self.homepoint)
				self.TextBufferChange(self, None)
				return

		if ((self.fssel.get_active_text()=="xfs") or (self.fssel.get_active_text()=="reiserfs")):
			self.fs = self.fssel.get_active_text() + " -f"
		else:
			self.fs = self.fssel.get_active_text()
		fs_txt = self.fssel.get_active_text()
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nStarting installation now.\n")
		self.TextBufferChange(self, None)
		mountpoint = "/mnt/" + self.partsel.get_active_text()[5:]
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Unmounting %s\n" % self.partsel.get_active_text())
		os.system ("umount %s" % self.partsel.get_active_text())
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Making ext3 filesystem on %s\n" %  self.partsel.get_active_text())
		os.system("mkfs -t %s %s" % (self.fs, self.partsel.get_active_text()))
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Making mount point for %s\n" %  self.partsel.get_active_text())
		os.system("mkdir %s" % mountpoint)
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Mounting %s " % self.partsel.get_active_text())
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "on %s\n" %mountpoint)
		os.system ("mount %s %s" % (self.partsel.get_active_text(), mountpoint))
		self.TextBufferChange(self, None)
		os.system ("mount > /tmp/mount.txt")
		file = open('/tmp/mount.txt')
		mount = file.read()
		file.close()
		mounted = False;
		lines = mount.split("\n", sys.maxint)
		for line in lines:
			word = line.split(None, sys.maxint)
			if (word.count("%s" % mountpoint)):
				mounted = True;
		if (mounted == False):
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "Fatal: Unable to mount %s." % mountpoint)
			resp = message.run()
			message.destroy()
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "Failed to mount %s\n" %mountpoint)
			self.TextBufferChange(self, None)
			return
		self.bootsel.set_sensitive(False)
		self.partsel.set_sensitive(False)
		self.homesel.set_sensitive(False)
		self.fssel.set_sensitive(False)
		self.swapsel.set_sensitive(False)
		self.button2.set_sensitive(False)
		self.button4.set_sensitive(False)
		self.button5.set_sensitive(False)
		self.button6.set_sensitive(False)
		self.button8.set_sensitive(False)
		
		thread.start_new_thread(self.progress_update, (self, self.wolvix_size))
		if (self.swapsel.get_active_text()!="None"):
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "Making new swap filesystem on %s\n" %self.swapsel.get_active_text())
			self.TextBufferChange(self, None)
			os.system("swapoff -a");
			os.system("mkswap %s" % self.swapsel.get_active_text());
			os.system("swapon -a");
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "Swap filesystem complete.\n")
			self.TextBufferChange(self, None)

		self.textbuffer.insert(self.textbuffer.get_end_iter(),
		"\nThe Wolvix system is now being copied to your hard disk...\
This may take some time, depending upon your hardware.\n\n")
		self.TextBufferChange(self, None)
		
		os.system ("mkdir %s/{boot,mnt,proc,sys,tmp}" % mountpoint)
		os.system ("cp /boot/vmlinuz %s/boot" % mountpoint)
		os.system ("cp -arP /media %s/" % mountpoint)
		dirlist = ['/bin', '/dev', '/etc', '/home', '/lib', '/root', '/sbin', '/usr', '/var', '/opt']
		for dir in dirlist:
			if (dir == '/home'):
				if (self.homesel.get_active_text()!="None"):
					os.system ("mkdir %s/home" % mountpoint)
					os.system ("cp -Rp %s/* %s" % (dir, self.homepoint))
					self.textbuffer.insert(self.textbuffer.get_end_iter(), "Copying %s/* to %s\n" % (dir, self.homepoint))
					self.TextBufferChange(self, None)
				else:
					self.textbuffer.insert(self.textbuffer.get_end_iter(), "Copying %s to %s\n" % (dir, mountpoint))
					os.system ("cp -Rp %s %s" % (dir, mountpoint))
					self.TextBufferChange(self, None)
			else:
				self.textbuffer.insert(self.textbuffer.get_end_iter(), "Copying %s to %s\n" % (dir, mountpoint))
				self.TextBufferChange(self, None)
				os.system ("cp -Rp %s %s" % (dir, mountpoint))
				self.TextBufferChange(self, None)
		os.system ("cp /boot/initrd.splash %s/boot" %mountpoint)
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nFinished copying directory structure\n")
		self.wolvix_size = (0.98*self.wolvix_size)
		self.TextBufferChange(self, None)
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nPopulating /mnt\n")
		os.system ("ls /mnt >/tmp/mnt.txt")
		file = open('/tmp/mnt.txt')
		mnt = file.read()
		file.close()
		lines = mnt.split("\n", sys.maxint)
		for line in lines:
			word = line.split(None, sys.maxint)
			if (self.homesel.get_active_text()):
				homesel = self.partsel.get_active_text()[5:]
			else:
				homesel = "snurd"
			if (word.count("live") or word.count(self.partsel.get_active_text()[5:]) or word.count(homesel)):
				self.TextBufferChange(self, None)
			else:
				path = mountpoint + "/mnt/" + line
				self.textbuffer.insert(self.textbuffer.get_end_iter(), "Making %s\n" % (path))
				os.system("mkdir %s" % path)
				self.TextBufferChange(self, None)
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "Completed populating /mnt\n")
		self.TextBufferChange(self, None)
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nModifying system files...\n")
		self.TextBufferChange(self, None)

		self.enable_gui(self, mountpoint)
		
		os.system("mv %s/etc/rc.d/rc.4.original %s/etc/rc.d/rc.4" %(mountpoint, mountpoint))
		os.system("mv %s/etc/rc.d/rc.6.original %s/etc/rc.d/rc.6" %(mountpoint, mountpoint))
		os.system("mv %s/etc/rc.d/rc.S.original %s/etc/rc.d/rc.S" %(mountpoint, mountpoint))
		os.system("mv %s/etc/rc.d/rc.M.original %s/etc/rc.d/rc.M" %(mountpoint, mountpoint))
		os.system("mv %s/etc/rc.d/rc.alsa.original %s/etc/rc.d/rc.alsa" %(mountpoint, mountpoint))
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "/etc/rc.d/ modifications complete\n")
		self.TextBufferChange(self, None)

		os.system("rm %s/etc/mtab" % mountpoint)
				
		file = open ('/etc/fstab')
		fstab = file.read()
		file.close()
		found_root = False;
		found_home = False;
		found_swap = False;
		os.unlink("%s/etc/fstab" % mountpoint)
		file = open("%s/etc/fstab" % mountpoint, 'w')
		lines = fstab.split("\n", sys.maxint)
		for line in lines:
			word = line.split(None, sys.maxint)
			if (word.count("tmpfs")):
				line = "# Wolvix installer removed tmpfs mount" 
			if (word.count("aufs")):
				line = "# Wolvix installer removed aufs mount" 
			if (word.count("%s" % self.partsel.get_active_text())):
				found_root = True
				line = "%s / %s auto,users,suid,dev,exec 1 1\n" % (self.partsel.get_active_text(), fs_txt)
			if (self.swapsel.get_active_text()!="None"):
				if (word.count("swap")):
					found_swap = True
					line = "%s swap swap swap 0 0\n" % self.swapsel.get_active_text()
			if (self.homesel.get_active_text()!="None"):
				if (word.count("%s" % self.homesel.get_active_text())):
					found_home = True
					line = "%s /home %s auto,users,rw,exec 0 0\n" % (self.homesel.get_active_text(), fs_txt)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nWrite to fstab: %s" % line)
			self.TextBufferChange(self, None)
			file.write("%s\n" % line)
		if (not(found_root)):
			line = "%s / %s auto,users,suid,dev,exec 0 0\n" % (self.partsel.get_active_text(), fs_txt)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nWrite to fstab: %s" % line)
			self.TextBufferChange(self, None)
			file.write("%s\n" % line)
		if (not(found_home) and self.homesel.get_active_text()!="None"):
			line = "%s /home %s auto,users,rw 0 0\n" % (self.homesel.get_active_text(), fs_txt)
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nWrite to fstab: %s" % line)
			self.TextBufferChange(self, None)
			file.write("%s\n" % line)
		if (not(found_swap) and self.partsel.get_active_text()!="None"):
			line = "%s swap swap swap 0 0\n" % self.swapsel.get_active_text()
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nWrite to fstab: %s" % line)
			self.TextBufferChange(self, None)
			file.write("%s\n" % line)
		file.close()
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "/etc/fstab entries complete\n")
		self.TextBufferChange(self, None)

		if (self.button2.get_active()):
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "Configuring GRUB boot loader ...\n")
			grub_config(mountpoint, self.bootsel.get_active_text(), "hd", False, self.wolvix_name)
		else:
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nNo bootloader selected to write to MBR.\n")
			self.textbuffer.insert(self.textbuffer.get_end_iter(), "You'll need to add wolvix to your bootloader later.\n")
			self.TextBufferChange(self, None)
		self.TextBufferChange(self, None)
		file = open("%s/var/log/installer.log"  % mountpoint, 'w')
		file.write(self.textbuffer.get_text(self.textbuffer.get_start_iter(),  self.textbuffer.get_end_iter(), True))
		file.close()
		self.textbuffer.insert(self.textbuffer.get_end_iter(), "\nInstallation is complete. You may now reboot into your new system.\n")
		self.TextBufferChange(self, None)
		self.bootsel.set_sensitive(True)
		self.partsel.set_sensitive(True)
		self.homesel.set_sensitive(True)
		self.fssel.set_sensitive(True)
		self.swapsel.set_sensitive(True)
		self.button2.set_sensitive(True)
		self.button4.set_sensitive(True)
		self.button5.set_sensitive(True)
		self.button6.set_sensitive(True)
		self.button8.set_sensitive(True)
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
			"Installation is complete.\n\
You may now close the panel and reboot into your new Wolvix system.")
		resp = message.run()
		message.destroy()

	def Button6Click(self, widget, data=None):

		def close_help (self):
			window.destroy()

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_size_request(480, 410)
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_resizable(False)
		window.set_title("Wolvix LiveCD Installer Help")
		window.set_border_width(10)

		fixed = gtk.Fixed()

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_IN)
		sw.set_size_request(430, 320)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textbuffer = gtk.TextBuffer()
		textbuffer.set_text("Program to install Wolvix to hard disk\n\
\n\
License:	GNU General Public license\n\
Author: 	Chris Gallienne\n\
Date:		5th April 2006\n\
\n\
Note: This script was wholly written by me, but I have lifted ideas\n\
from various other installer shell scripts, principally the following:\n\
\n\
DamnSmallLinux dsl-hdinstall script, which was itself a modification \
of the KNOPPIX knx-hdinstall 0.37 by Christian Perle; the knoppix \
scripts 'knoppix-installer' by Fabian Franz and 'mkboot' by Guy Maor;\
the grub_config script of Patrick Volkerding; \
and the 'slax-installer' and 'slax-liloconfig' scripts by Thomas Matejicek.\n\
\n\
WARNING: This program is in development. Use it at your own risk! \n\n\
\n\
INSTALLATION:\n\
You must perform the following steps to use this installer:\n\n\
1: Select the device from which your system boots.\n\
This is normally the primary hard disk - if you elect to install a bootloader \
to the MBR (master boot record) it will be this partition to which it will be \
written.\n\n\
2: Select a target partition for wolvix.\n\
This is the root partition, to which the wolvix system will be copied. All \
data already on this partition will be lost. If you have not already prepared \
a partition for the Wolvix system you may do so by clicking on the 'Run gparted' \
button, and creating a partition using that tool. You may get some error messages \
from gparted, due to new partitions not being registered, but these may be ignored \
at this stage. After exiting the gparted utility the new partitioning scheme \
should be available within the installer. If not, close and restart the installer. \
You MAY have to reboot Wolvix before continuing, in order to register the \
changes with the kernel.\n\n\
3: Optionally, choose a separate partition to mount your '/home' directory. \
This will retain all user-related data and configuration in the event of a \
later re-installation of Wolvix. All existing data on this partition will \
be lost. If you choose not to exercise this option, the '/home' directory will \
reside in the root partition as usual. As above, the partition may be created \
using 'gparted', but any changes in partitioning will require a system reboot \
to register the changes with the kernel before continuing with the install. \n\n\
4: Select a swap partition. This is a disk partition used as virtual memory, i.e. \
an area of disk storage which appears to your system as extra RAM. A swap partition \
is not strictly necessary, but strongly recommended, especially if your conventional \
memory is limited, or if you use a lot of large, memory-intensive programmes. Some \
application programs are out there which expect to find a swap partition. There \
is no clear consensus about the size of swap partition, but a reasonable guide is \
1-2 times the size of your conventional memory - e.g. if you have 256MB of RAM, a \
swap partition of 512MB is a good choice.\n\n\
5: Select filesystem to use for your wolvix system. The default, and the recommended \
choice is 'ext3'. The 'xfs' option has been removed because it doesn't play nice \
with the GRUB bootloader. \n\n\
6. Choose bootloader options - if you choose not to install a bootloader to the \
hard disk (and you don't already have a bootloader which you can configure to boot \
Wolvix) you will need to make a boot disk. This is recommended in any case for use \
in emergencies. If GRUB is selected, it will detect all partitions on your \
system which appear to contain DOS, Windows or Linux operating systems. During the \
configuration of the bootloader, for each of these partitions you will be asked if \
you want to add it to the bootloader, and if so, to give it a recognisable name.\n\n\
7: Click 'Start Install' and go get a coffee while your Wolvix system is installed. \
this will take some time, depending upon the speed of your hardware. For example, \
on my Athlon 2400+ system the whole install process takes around 10 minutes\n\n\
8: Reboot. Enjoy!\n\n")
		textview.set_buffer(textbuffer)
		textview.show()
		sw.add(textview)
		sw.show()
		fixed.put(sw, 15, 15)

		button = gtk.Button("Close")
		button.set_size_request(80, 30)
		button.connect("clicked", close_help)
		button.show()
		fixed.put(button, 200, 355)
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
				self.homesel.append_text(word[0])
				self.swapsel.append_text(word[0])
			if (line.find("swap")>=0):
				word = line.split(None, sys.maxint)
				self.swapsel.prepend_text(word[0])
		self.partsel.set_active(0)
		self.homesel.set_active(0)
		self.swapsel.set_active(0)

	def close_application(self, widget, data=None):
		self.window.destroy()

	def get_wolvix_size(self, widget, data=None):
		wolvix_id = file('/etc/wolvix-version').readlines()
		self.wolvix_name = wolvix_id[0].strip()
		for dir in ['/bin', '/dev', '/etc', '/home', '/lib', '/root', '/sbin', '/usr', '/var', '/opt']:
			os.system("du -b -s %s >> /tmp/size.txt" %dir)
		for line in file('/tmp/size.txt').readlines():
			words = line.split(None, sys.maxint)
			self.wolvix_size += float(words[0])
		os.system("rm /tmp/size.txt")	
		self.textbuffer.insert(self.textbuffer.get_end_iter(), 
			"%s - Installed size = %s\n" %(self.wolvix_name, self.wolvix_size))
		self.TextBufferChange(self, None)
		print "%s - Installed size = %s\n" %(self.wolvix_name, self.wolvix_size)
		
	def renew_mountpoints(self, widget, data=None):
		children = self.leftbox.get_children()
		for child in children:
			self.leftbox.remove(child)
		self.make_leftbox(self, None)
	
        def make_leftbox(self, widget, data=None):
		image = gtk.Image()
		image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
		self.leftbox.pack_start(image, False, False, 5)
		image.show()

		label1 = gtk.Label("1:Boot device:")
		label1.set_line_wrap(True)
		self.leftbox.pack_start(label1, False, False, 0)
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
		self.leftbox.pack_start(self.bootsel, False, False, 0)
		self.bootsel.show()
		self.partsel = gtk.combo_box_new_text()
		self.partsel.set_size_request(100, 30)
		self.homesel = gtk.combo_box_new_text()
		self.homesel.set_size_request(100, 30)
		self.swapsel = gtk.combo_box_new_text()
		self.swapsel.set_size_request(100, 30)
		self.homesel.append_text("None")
		self.swapsel.append_text("None")
		self.populate(self, None)
		label2 = gtk.Label("2:Root partition:")
		label2.set_line_wrap(True)
		label3 = gtk.Label("3:Optional: /home:")
		label3.set_line_wrap(True)
		self.fssel = gtk.combo_box_new_text()
		self.fssel.set_size_request(100, 30)
		self.fssel.append_text("ext2")
		self.fssel.append_text("ext3")
		self.fssel.append_text("reiserfs")
		#self.fssel.append_text("xfs")
		label4 = gtk.Label("4:Swap partition:")
		label4.set_line_wrap(True)
		label5 = gtk.Label("5:Select filesystem:")
		label5.set_line_wrap(True)
		self.button2 = gtk.CheckButton("6: Install GRUB")
		self.button2.connect("toggled", self.Button2Click, "GRUB")
		
		self.leftbox.pack_start(label2, False, False, 0)
		self.leftbox.pack_start(self.partsel, False, False, 0)
		self.leftbox.pack_start(label3, False, False, 0)
		self.leftbox.pack_start(self.homesel, False, False, 0)
		self.leftbox.pack_start(label4, False, False, 0)
		self.leftbox.pack_start(self.swapsel, False, False, 0)
		self.leftbox.pack_start(label5, False, False, 0)
		self.leftbox.pack_start(self.fssel, False, False, 0)
		self.leftbox.pack_start(self.button2, False, False, 0)
		label2.show()
		label3.show()
		label4.show()
		label5.show()
		self.fssel.set_active(1)
		self.partsel.show()
		self.homesel.show()
		self.swapsel.show()
		self.fssel.show()
		self.button2.show()
		self.leftbox.show()
		
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
		self.homepoint = ""
		self.partitionok = False
		self.last_percent=0
		self.size=""
		self.fs = "ext3"
		self.used = "0"
		self.timer = gobject
		self.space=0
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#self.window.set_size_request(560, 560)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_resizable(True)

		self.window.connect("destroy", self.close_application)
		self.window.set_title("Wolvix LiveCD Hard Disk Installer")
		self.window.set_border_width(10)

		self.mainbox = gtk.VBox(False, 0)
		self.topbox = gtk.HBox(False, 0)
		
		self.leftbox = gtk.VBox(False, 5)
		self.make_leftbox(self, None)
		
		self.rightbox = gtk.VBox(False, 10)
		self.sw = gtk.ScrolledWindow()
		self.sw.set_shadow_type(gtk.SHADOW_IN)
		self.sw.set_size_request(330, 320)
		self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		self.textbuffer = gtk.TextBuffer()
		self.textbuffer.set_text("This is the Wolvix LiveCD hard disk installer. \
This utility is in development...Use with care!\n\n\
This installation log will be saved to /var/log/installer.log \
on your new system after the installer completes. If you have a \
problem, read this file as a first step to finding what went wrong.\n\n\
You must perform the following steps to use this installer:\n\n\
1: Select the device from which your system boots.\n\n\
2: Select a target partition for wolvix.\n\
(Run the gparted utility if you need to create/view partitions).\n\n\
3: Optionally, you may choose to locate your home directory on a separate \
partition. This will enable you to keep all your personal settings & files \
if you reinstall Wolvix at a later date.\n\n\
4: Select a swap partition - not strictly necessary, but strongly recommended.\n\n\
5: Select filesystem to use - if you're not sure, ext3 is a good choice. \n\n\
6: Choose bootloader options - if you choose not to install a bootloader \
to the hard disk (and you don't already have a bootloader which you can \
configure to boot Wolvix) you will need to make a boot disk. This is recommended \
in any case for use in emergencies.\n\n\
7: Click 'Start Install' and go get a coffee while your Wolvix system is installed.\n\n\
8: Reboot. Enjoy!\n\n")
		self.textbuffer.connect("changed", self.TextBufferChange, None)
		self.textview.set_buffer(self.textbuffer)
		self.sw.add(self.textview)
		self.rightbox.pack_start(self.sw, True, True, 10)
		self.sw.show()
		self.textview.show()
		self.topbox.pack_start(self.leftbox, False, False, 10)
		self.topbox.pack_end(self.rightbox, True, True, 10)
		self.leftbox.show()
		self.rightbox.show()
		self.partsel.connect("changed", self.PartSelClick, None)
		self.homesel.connect("changed", self.HomeSelClick, None)
		self.swapsel.connect("changed", self.SwapSelClick, None)
		self.fssel.connect("changed", self.FSSelClick, None)

		self.middlebox = gtk.HBox(False, 10)
		self.pbar = gtk.ProgressBar()
		self.middlebox.pack_start(self.pbar, True, True, 10)
		self.pbar.show()
		
		self.bottombox = gtk.HBox(False, 10)
		self.button4 = gtk.Button("Run gparted?")
		self.button4.set_size_request(110, 30)
		self.button4.connect_object("clicked", self.Button4Click, self.window, None)
		self.button4.set_flags(gtk.CAN_DEFAULT)
		self.bottombox.pack_start(self.button4, True, False, 10)
		self.button4.show()
		self.button5 = gtk.Button("7: Start Install")
		self.button5.set_size_request(110, 30)
		self.button5.connect("clicked", self.Button5Click)
		self.bottombox.pack_start(self.button5, True, False, 10)
		self.button5.show()
		self.button6 = gtk.Button("Help")
		self.button6.set_size_request(110, 30)
		self.button6.connect("clicked", self.Button6Click)
		self.bottombox.pack_start(self.button6, True, False, 10)
		self.button6.show()
		self.button8 = gtk.Button("Close")
		self.button8.set_size_request(110, 30)
		self.button8.connect("clicked", self.close_application)
		self.button8.set_flags(gtk.CAN_DEFAULT)
		self.bottombox.pack_start(self.button8, True, False, 10)
		self.button8.show()

		self.mainbox.pack_start(self.topbox, True, True, 0)
		self.topbox.show()
		self.mainbox.pack_start(self.middlebox,  False, False, 10)
		self.middlebox.show()
		self.mainbox.pack_start(self.bottombox, False, False, 0)
		self.bottombox.show()

		self.window.add(self.mainbox)
		self.mainbox.show()
		self.window.show()

		self.get_wolvix_size(None)

def main():
	uid = os.getuid()
	if (uid != 0):
		mb = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Sorry, you must have root\nprivileges to run this program.");
		response = mb.run()
	else:
		gtk.main()
	return 0

if __name__ == "__main__":
	WolvixInstall()
	main()
