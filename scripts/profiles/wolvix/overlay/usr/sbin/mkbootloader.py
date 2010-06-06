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

def list_partitions ():
        for devs in ['/dev/hda', '/dev/hdb', '/dev/hdc', '/dev/hdd', '/dev/hde', '/dev/hdf', '/dev/hdg',
            '/dev/hdh', '/dev/hdi', '/dev/hdj', '/dev/hdk', '/dev/hdl', '/dev/hdm', '/dev/hdn', '/dev/hdo',
            '/dev/hdp', '/dev/sda', '/dev/sdb', '/dev/sdc', '/dev/sdd', '/dev/sde', '/dev/sdf', '/dev/sdg',
            '/dev/sdh', '/dev/sdi', '/dev/sdj', '/dev/sdk', '/dev/sdl', '/dev/sdm', '/dev/sdn', '/dev/sdo', '/dev/sdp']:
            os.system("fdisk -l %s >>/tmp/devs.txt" % devs)

def get_fb_console():								# Use framebuffer console modes ?
	use_fb = ""
	use_fb =not(os.system("grep '29 fb' /proc/devices >/tmp/fb.txt"))
	if (use_fb):									# Kernel support for framebuffer console?
		line_ask = gtk.Dialog("Use framebuffer?", None, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		line_ask.set_position(gtk.WIN_POS_CENTER)
		help = gtk.Label("\nYour kernel has support for frame buffer console.\n\
This allows more rows and columns of text on screen,\n\
but is slower than the standard console, and not all\n\
video cards support it. Select frame buffer resolution\n\
or standard console:\n")
		help.show()
		line_ask.vbox.pack_start(help, True, True, 0)
		select1 = gtk.RadioButton(None, "Standard Console - (safe choice)", False)
		select1.show()
		line_ask.vbox.pack_start(select1, True, True, 0)
		select2 = gtk.RadioButton(select1, "640x480 - 65k colours", False)
		select2.show()
		line_ask.vbox.pack_start(select2, True, True, 0)
		select3 = gtk.RadioButton(select1, "800x600 - 65k colours", False)
		select3.show()
		line_ask.vbox.pack_start(select3, True, True, 0)
		select4 = gtk.RadioButton(select1, "1024x768 - 65k colours", False)
		select4.show()
		line_ask.vbox.pack_start(select4, True, True, 0)
		select5 = gtk.RadioButton(select1, "1280x1024 - 65k colours", False)
		select5.show()
		line_ask.vbox.pack_start(select5, True, True, 0)
		response = line_ask.run()
		if (select2.get_active()):
			fb = 785
		elif (select3.get_active()):
			fb = 788
		elif (select4.get_active()):
			fb = 791
		elif (select5.get_active()):
			fb = 794
		else:
			fb = 0								# choice, or default, don't use framebuffer
		line_ask.destroy()
	return fb 

def grub_config(mountpoint, bootpoint, target, cdboot, wolvix_name):
# mount point: 	install directory (e.g. /mnt/hda1)
# bootpoint: 		boot device: target device (e.g. /dev/hda)
# target: 		"hd" or "fd"
# cdboot:		grub option to boot from cdrom
	fb = get_fb_console()
        list_partitions() 								# What's available? > /tmp/devs.txt
        os.system("mkdir %s/boot/grub" % mountpoint)	# Make a 'menu.lst' for GRUB
        ofile = open("%s/boot/grub/menu.lst" % mountpoint, 'w')
        ofile.write("# menu.lst created by wolvix-installer\n")
        ofile.write("# See: grub(8), info grub, update-grub(8),\n")
        ofile.write("#      grub-install(8), grub-floppy(8),\n")
        ofile.write("# \n")
        ofile.write("# default num\n")
        ofile.write("# the nuber of the default entry\n")
        ofile.write("# '0' is the defauly if none specified\n")
        ofile.write("default 0\n")
        ofile.write("# \n")
        ofile.write("# \n")
        ofile.write("# timeout sec\n")
        ofile.write("# The delay before the default entry is booted\n")
        ofile.write("timeout 10\n")
        ofile.write("# \n")
        ofile.write("# \n")
        ofile.write("# Pretty colours\n")
        ofile.write("color cyan/blue white/blue\n")
        ofile.write("# \n")
        ofile.write("# \n")
        ofile.write("# password ['--md5'] passwd\n")
        ofile.write("""# If used in the first section of a menu file, disable all interactive editing
# control (menu entry editor and command-line)  and entries protected by the
# command 'lock'""")
        ofile.write("# e.g. password topsecret\n")
        ofile.write("#      password --md5 $1$gLhU0/$aW78kHK1QfV3P2b2znUoe/\n")
        ofile.write("# password topsecret\n")
        ofile.write("# \n")
        ofile.write("#\n")
        ofile.write("# examples\n")
        ofile.write("#\n")
        ofile.write("# title		Windows 95/98/NT/2000\n")
        ofile.write("# root			(hd0,0)\n")
        ofile.write("# makeactive\n")
        ofile.write("# chainloader	+1\n")
        ofile.write("#\n")
        ofile.write("# title		Linux\n")
        ofile.write("# root			(hd0,1)\n")
        ofile.write("# kernel		/vmlinuz root=/dev/hda2 ro\n")
        ofile.write("#\n")
        ofile.write("# \n")
        os.system("fdisk -l >/tmp/devs.txt")
        ifile = open("/tmp/devs.txt")
        devs = ifile.read()
        ifile.close()
        os.system("rm /tmp/devs.txt")
        lines = devs.split("\n", sys.maxint)					# Make a list of partitions available
        for line in lines:
            word = line.split(None, sys.maxint)
            if ((word.count("Linux") and (not(word.count("swap")))) or word.count("HPFS/NTFS") or  word.count("DOS") or word.count("Win") or word.count("W95") or word.count("FAT16")):
                frugal = False
		line_ask = gtk.Dialog("Select boot options", None, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                line_ask.set_position(gtk.WIN_POS_CENTER)			# If it seems to have an operating system
                help = gtk.Label("Found partition which appears to contain \n\
an operating system - do you wish this \n\
partition appear at boot time? If so, \n\
check it and give it a (short) name \n\
(no whitespace):\n\
(If you're unsure, check & name it anyway)")
                help.show()
                line_ask.vbox.pack_start(help, True, True, 0)
                hbox = gtk.HBox(False, 0)
                select1 = gtk.CheckButton("%s" % word[0][5:])
                hbox.pack_start(select1, True, True, 0)
                select1.show()
                enter1 = gtk.Entry()
                enter1.set_max_length(26)
                
		if (word[0][5:] == mountpoint[5:]):
			enter1.set_text("%s" % wolvix_name)
		else:
			enter1.set_text("%s-%s" % (word[0][5:], word[5]))
                hbox.pack_start(enter1, True, True, 0)
                enter1.show()
                line_ask.vbox.pack_start(hbox, True, True, 0)
                hbox.show()
        
                os.system("ls /mnt/%s >/tmp/root.txt" % word[0][5:])
                file=open("/tmp/root.txt")
                root = file.read()
                file.close()
                select1.set_active(False)
                contents = root.split("\n", sys.maxint)
		if ((contents.count("MSDOS.SYS")) or (contents.count("msdos.sys"))or (contents.count("boot"))or (contents.count("command.com"))):			
                        response = line_ask.run()
                        if (select1.get_active()):
                            if (word.count("Linux") and (not(word.count("swap")))):
				if (contents.count("wolvix")):
					frugal = True
				if (fb):
                                    fb_use = "vga=%s" % str(fb)
                                else:
                                    fb_use = ""
                                ofile.write("\n")
                                ofile.write("title			%s\n" % enter1.get_text())
                                dev = ord(word[0][7:8])-97
                                length = len(word[0])			# cope with partitions > 10
				part = int(word[0][8:length])-1
				mount = "/mnt/" + word[0][5:]
				os.system("ls %s/boot > /tmp/boot.txt" % mount)
				file = open('/tmp/boot.txt')
				boot = file.read()
				file.close()
				has_initrd = False
				has_initrd_splash = False
				bootlines = boot.split("\n", sys.maxint)
				vmlinuz = "vmlinuz"
				initrd_splash = ""
				for bootline in bootlines:
					if (bootline.count("initrd.img")):
						has_initrd = True
						initrd = bootline
					elif (bootline.count("initrd.splash")):
						has_initrd_splash = True
						initrd_splash = "splash=silent"
					elif (bootline.count("vmlinuz")):
						vmlinuz = bootline
				ofile.write("root			(hd%s,%s)\n" % (dev, part))
                                if (frugal):						# Poorman's GRUB line
					ofile.write("kernel			/boot/vmlinuz root=/dev/ram0 rw load_ramdisk=1 prompt_ramdisk=1 ramdisk_size=6666 max_loop=255 vga=791\n")
					ofile.write("initrd			/boot/initrd.gz\n")
                                else:						# Normal GRUB line
					ofile.write("kernel			/boot/%s root=%s %s %s %s\n" % (vmlinuz, word[0], "ro", fb_use, initrd_splash))
				if ((has_initrd) and not(frugal)):	# Some distros use initrd
					ofile.write("initrd			/boot/%s\n" % initrd) 
				if ((has_initrd_splash) and not(frugal)):	# Some distros use initrd
					ofile.write("initrd			/boot/initrd.splash\n")
                        	ofile.write("savedefault\n")
                                ofile.write("boot\n")
                            if (word.count("HPFS/NTFS") or  word.count("DOS") or word.count("Win") or word.count("W95") or word.count("FAT16")):
                                ofile.write("\n")
                                ofile.write("title 			%s\n" % enter1.get_text())
                                dev = ord(word[0][7:8])-97
                                length = len(word[0])
				print "Word length = %s" % length
				part = int(word[0][8:length])-1
				print "Partition = (hd%s,%s)" % (dev, part)
				ofile.write("root   		(hd%s,%s)\n" % (dev, part))
                                ofile.write("savedefault\n")
                                ofile.write("makeactive\n")
                                ofile.write("chainloader	+1\n")
                        line_ask.destroy()
        if (cdboot):
            ofile.write("\n")
            ofile.write("title 		Boot from CDROM \n")
            ofile.write("kernel 		/boot/grub/memdisk.bin \n")
            ofile.write("initrd		/boot/grub/sbootmgr.dsk \n")
        ofile.close()

        if (target == "fd"):
            message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, 
                "Insert floppy disk to use as boot disk, and click 'OK'\n WARNING: All data will be destroyed!") 
            message.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
            message.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
            resp = message.run()
            message.destroy()
            if (resp == gtk.RESPONSE_ACCEPT):
                os.system("mkfs.ext2 /dev/fd0")
                os.system("grub-install --root-directory=%s '(fd0)'" % mountpoint)
            else:
                return(0)
        
	if (target == "hd"):
            print "\nInstalling GRUB to %s, root = %s\n\n" %(bootpoint, mountpoint)
            os.system("grub-install --no-floppy --root-directory=%s %s" % (mountpoint, bootpoint))
        return(1)
        
        
        return(1)
