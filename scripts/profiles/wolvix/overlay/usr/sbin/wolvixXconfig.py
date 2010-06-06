#!/usr/bin/env python
#
# Program to configure x-org for Wolvix
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
import gtk, gobject, os, sys, time
import re, os.path, shutil

from changekeybd import *

class WolvixXconfig:

	def HelpClick(self, widget, data=None):

		def close_help (self):
			window.destroy()

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_size_request(480, 490)
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_resizable(False)
		window.set_title("Wolvix X-Configuration Help")
		window.set_border_width(10)

		fixed = gtk.Fixed()

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_IN)
		sw.set_size_request(430, 400)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textbuffer = gtk.TextBuffer()
		textbuffer.set_text("Program to configure X-windows hardware\n\
\n\
License:	GNU General Public license\n\
Author: 	Chris Gallienne\n\
Date:	30th September 2006\n\
\n\
WARNING: This program is in development. Use it at your own risk! \n\n\
USAGE:\n\
There are several ways to use this utility: \n\n\
1. The system correctly detects all your hardware. You test it, it works, \
You accept the results & use your new configuration. \n\n\
2. You select a mode from the list that you believe your \
hardware capable of. You test it. It works - as above. \n\n\
3: You are an adventurous soul and you want to try a more \
demanding mode - test, etc. It doesn't work - you select \
a less demanding mode and try again.\n\n\
Note: If you accept the new settings, a new xorg.conf file \
will be generated. You will therefore be prompted to enter a \
keyboard layout to be written to this file. Please select your \
keyboard layout and check the 'make permanent' box.")
		textview.set_buffer(textbuffer)
		textview.show()
		sw.add(textview)
		sw.show()
		fixed.put(sw, 15, 15)

		button = gtk.Button("Close")
		button.set_size_request(80, 30)
		button.connect("clicked", close_help)
		button.show()
		fixed.put(button, 200, 430)
		fixed.show()
		window.add(fixed)

		window.show()

	def ResSelClick(self, widget, data=None):
		index=self.ressel.get_active()
		word = self.modelist[index].split(None, sys.maxint)
		full_h = float(word[6])
		full_v = float(word[10])
		pixclock = 1000000.0*float(word[2])
		vfreq = pixclock/(full_h*full_v)
		hfreq = pixclock/(full_h*1000)
		self.refsel1.set_text(str(round(40))) 
		self.hfreqsel1.set_text(str(round(30))) 
		self.refsel2.set_text(str(round(vfreq))) 
		self.hfreqsel2.set_text(str(round(hfreq))) 
		self.UpdateMode(self, None)
		return
	
	def close_application(self, widget, data=None):
		self.window.destroy()

	def set_best_res(self, widget, data=None):
		
		return
		
	def ask_monitor(self, widget, data = None):
		
		def close_help (self):
			window.destroy()
		
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_size_request(360, 390)
		window.set_resizable(False)
		window.set_title("Wolvix X-config Information")
		window.set_border_width(10)

		fixed = gtk.Fixed()

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_IN)
		sw.set_size_request(320, 310)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textbuffer = gtk.TextBuffer()
		textbuffer.set_text("Unable to determine your monitor type.\n\
\n\
This may be because you are using a notebook computer, \
or simply because your monitor is not in the database. \n\n\
Choose from the list of modes one which you think your \
monitor capable of. Test it. If successful you may use \
this mode, or try another one. If the test fails, try a \
less demanding mode until you find the optimal one.\n\n\
WARNING: By all means, experiment with this utility \
to see how far can go with your hardware. Most monitors \
can be overdriven a little. But have a care: Begin with \
conservative settings. Some monitors can be permanently \
damaged by too high a refresh rate! If you blow it up, \
you get to keep all the pieces!")
		textview.set_buffer(textbuffer)
		textview.show()
		sw.add(textview)
		sw.show()
		fixed.put(sw, 15, 15)

		button = gtk.Button("Close")
		button.set_size_request(80, 30)
		button.connect("clicked", close_help)
		button.show()
		fixed.put(button, 140, 340)
		fixed.show()
		window.add(fixed)

		window.show()
		return
		
	def SetBits(self, widget, data = None):
		count = 0
		index = self.ressel.get_active()
		words = self.modelist[index].split(None, sys.maxint)
		hres = float(words[3])
		vres = float(words[7])
		mem = self.graphicmem.get_text()
		bytes = 1024.0*float(mem)/(float(vres)*float(hres))
		if (bytes>3):
			self.depthsel.set_text("24")
		elif (bytes>2):
			self.depthsel.set_text("16")
		elif (bytes>1):
			self.depthsel.set_text("8")
		else:
			self.depthsel.set_text("4")
		
	def UpdateMode(self, widget, data=None):
		self.good_modes = []
		index = self.ressel.get_active()
		words = self.modelist[index].split(None, sys.maxint)
		h_res = int(words[3])
		v_res = int(words[7])
		for mode in self.modelist:
			if ((mode != "") and (mode.count("pclk")<1)):
				word = mode.split(None, sys.maxint)
				hres = int(word[3])
				vres = int(word[7])
				if (hres < h_res) and (vres < v_res):
					mode_item = "%sx%s" % (hres, vres)
					if self.good_modes.count(mode_item)<1:
						self.good_modes.append(mode_item)
		mode_item = "%sx%s" % (h_res, v_res)
		self.good_modes.append(mode_item)
		self.good_modes.reverse()
		self.SetBits(self, data=None)
		return
	
	def InitValues(self, widget, data=None):
		standard = 12
		os.system('ddcprobe > /tmp/ddcprobe.txt')
		file = open("/tmp/ddcprobe.txt")
		ddcprobe = file.read()
		file.close()
		lines = ddcprobe.split("\n", sys.maxint)
		for line in lines:
			if (line.count("Memory installed")):
				word = line.split(None, sys.maxint)
				self.graphicmem.set_text(word[8].replace('kb', ''))
		os.system("mkxcfg -d >/tmp/video.txt")
		file = open("/tmp/video.txt")
		video_data = file.read()
		file.close()
		lines = video_data.split("\n", sys.maxint)
		for line in lines:
			if (line.count("Video")):
				index = 15
				card_name = ''
				while line[index] <> '|':
					card_name = card_name + line[index]
					index = index + 1
					#word = line.split(None, sys.maxint)
				self.cardsel.append_text(card_name)
				#self.cardsel.append_text(word[2]+' '+word[3])
			self.cardsel.set_active(0)
			if (line.count("Monitor")):
				word = line.split(None, sys.maxint)
				self.monitorsel.append_text(word[2]+' '+word[3])
			self.monitorsel.set_active(0)
		os.system("hwd -e >/tmp/hwd.txt")
		file = open("/tmp/hwd.txt")
		hwdata = file.read()
		file.close()
		lines = hwdata.split("\n", sys.maxint)
		for line in lines:
			if (line.count("Mouse") and line.count(':')):
				mouse = ''
				index = 0
				length = len(line)
				while line[index]<>':':
					index = index + 1
				index = index + 1
				while index<length:
					mouse = mouse + line[index]
					index = index + 1
				mouse.lstrip()
				self.mousesel.append_text(mouse)
			self.mousesel.set_active(0)
		os.system('ls /usr/X11/lib/modules/drivers > /tmp/drivers.txt')
		file = open("/tmp/drivers.txt")
		drivers = file.read()
		file.close()
		lines = drivers.split("\n", sys.maxint)
		index = 0
		self.driversel.append_text("Not Found")
		driver_index = 0
		for line in lines:
			if (line != ""):
				line = line.replace('.so', '')
				line = line.replace('_drv', '')
				self.driversel.append_text(line)
				card = str(self.cardsel.get_active_text())
				card = card.lower()
				index = index + 1
				if (card.find(line)>=0):
					driver_index = index
		self.driversel.set_active(driver_index)
		os.system('ddcxinfo-arch -monitor > /tmp/modes.txt')
		file = open("/tmp/modes.txt")
		modes = file.read()
		file.close()
		lines = modes.split("\n", sys.maxint)
		index = 0
		driver_index = 0
		for line in lines:
			if ((line.count("# 640") or line.count("# 720") or line.count("# 800") or line.count("# 1024") or 
				line.count("# 1152") or line.count("# 1280") or line.count("# 1400") or line.count("# 1600")) and (line.count("pclk")<1)):
				line = line.replace("	# ", "")
				line = line.replace("(industry standard)", "")
				line = line.replace("(Industry standard)", "")
				self.ressel.append_text(line)
			elif (line.count('ModeLine')):	
				self.modelist.append(line)
		self.ressel.set_active(standard)
		word = self.modelist[standard].split(None, sys.maxint)
		hres = float(word[6])
		vres = float(word[10])
		pixclock = 1000000.0*float(word[2])
		vrate = pixclock/(hres*vres)
		hrate = pixclock/(hres*1000)
		self.refsel1.set_text(str(round(40))) 
		self.hfreqsel1.set_text(str(round(30))) 
		self.refsel2.set_text(str(round(vrate))) 
		self.hfreqsel2.set_text(str(round(hrate))) 
		
		lines = ddcprobe.split("\n", sys.maxint)
		index = 0
		name = ""
		for line in lines:
			if (line.count("Monitor details 1:")):
				index = 5
				found = True
			if (index > 0):
				if (line.count("Name:")):
					words = line.split(None, sys.maxint)
					for word in words:
						if (word.count("Name")<1):
							self.found = True
							name = name + ' ' +word
					self.monitorsel.append_text(name)
					self.monitorsel.set_active(1)
				if(line.count("Timing ranges:")):
					words = line.split(None, sys.maxint)
					self.refsel1.set_text(words[4])
					self.refsel2.set_text(words[6].replace(',', ''))
					self.hfreqsel1.set_text(words[9])
					self.hfreqsel2.set_text(words[11])
					self.set_best_res(self, None)
					self.UpdateMode(self, None)
			index = index - 1		
		self.UpdateMode(self, None)
		self.SetBits(self, None)
		
	def TestConfig(self, widget, data = None):
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
		"A new x-session will start in another virtual terminal to \
enable you to check  your x-configuration. After testing you may exit \
as normal from menu. If the session is unusable, press 'ctrl-alt-backspace' \
to kill the session and return here.")
		resp = message.run()
		message.destroy()

		os.system('cp /etc/X11/xorg.conf /etc/X11/xorg.conf.wcp')
		os.system('cp /etc/X11/xorg.conf-vesa /etc/X11/xorg.conf')
		file = open('/etc/X11/xorg.conf')
		conf = file.read()
		file.close()
		file = open('/etc/X11/xorg.conf', 'w')
		lines = conf.split("\n", sys.maxint)
		for line in lines:
			if line.count('Section "Monitor"'):
				file.write('# Section added by Wolvix Control Panel\n\n')
				file.write('Section "Monitor"\n')
				file.write('   Identifier "%s"\n' % self.monitorsel.get_active_text())
				file.write('   HorizSync %s-%s\n' % (self.hfreqsel1.get_text(), self.hfreqsel2.get_text()))
				file.write('   VertRefresh %s-%s\n'% (self.refsel1.get_text(), self.refsel2.get_text()))
				file.write('EndSection\n\n\n')
			if line.count('Section "Device"'):
				file.write('# Section added by Wolvix Control Panel\n\n')
				file.write('Section "Device"\n')
				file.write('   Identifier "%s"\n' % self.cardsel.get_active_text())
				file.write('   Driver     "%s"\n' % self.driversel.get_active_text())
				file.write('   VideoRam    %s\n'% self.graphicmem.get_text())
				file.write('EndSection\n\n\n')
			if line.count('Section "Screen"'):
				file.write('# Section added by Wolvix Control Panel\n\n')
				file.write('Section "Screen"\n')
				file.write('   Identifier "WCPScreen"\n')
				file.write('   Device     "%s"\n' % self.cardsel.get_active_text())
				file.write('   Monitor    "%s"\n' % self.monitorsel.get_active_text())
				file.write('   DefaultDepth %s\n\n' % self.depthsel.get_text())
				file.write('   Subsection "Display"\n')
				file.write('      Depth    %s\n' % self.depthsel.get_text())
				mode_str = '      Modes  '
				for mode in self.good_modes:
					mode_str = mode_str + '"%s" ' % mode
				mode_str = mode_str + "\n"
				file.write(mode_str)
				file.write("   EndSubsection\n\n")
				file.write('EndSection\n\n\n')
			if line.count('Screen "Screen 1"'):
				line = 'Screen "WCPScreen"\n\n'
			file.write("%s\n" % line)
		file.close()
		xinit = "#!/bin/bash\n/usr/X11R6/bin/xset c off s 600\nsleep 2\n/usr/X11R6/bin/xsetroot -gray\n\
/usr/X11R6/bin/xterm &\n/usr/bin/fluxbox  -display :1.0"
		file = open('/etc/X11/xinit/xinitrc2', 'w')
		file.write(xinit)
		file.close()
		os.system("/usr/X11R6/bin/startx /etc/X11/xinit/xinitrc2 -- :1")
		os.system("exit")

		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                "Did the x-session display ok? Are you happy \
with this configuration?")
		resp = message.run()
		if (resp == gtk.RESPONSE_YES):
			self.testOK = True
		else:
			self.testOK = False
		message.destroy()
		if (self.testOK):
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
			"A new xorg.conf has been written to /etc/X11. \
Your old xorg.conf file was saved as xorg.conf.wcp. \
If you have a problem running x-windows, you can \
restore it by copying it back to /etc/X11/xorg.conf. \
You may now close the Wolvix-X-Configurator & restart \
X-windows with your new configuration if you wish.")
			resp = message.run()
			message.destroy()	
			change_keybd()
		else:
			os.system('mv /etc/X11/xorg.conf.wcp /etc/X11/xorg.conf')
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
			"OK, your original xorg.conf file has been restored. \
You can change to more conservative selections \
and try again, or keep your existing configuration.")
			resp = message.run()
			message.destroy()	
			
	def __init__(self):
		self.found = False
		self.modelist = []
		self.good_modes = []
		gtk.rc_parse("/etc/gtk/gtkrc.iso-8859-2")
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_resizable(True)
		self.testOK = False

		self.window.connect("destroy", self.close_application)
		self.window.set_title("Wolvix X-configurator")
		self.window.set_border_width(10)

		self.mainbox = gtk.VBox(False, 10)
		self.topbox = gtk.HBox(False, 10)
		self.genbox = gtk.HBox(False, 10)
		self.simplebox = gtk.HBox(False, 10)
		self.expertbox = gtk.HBox(False, 10)
		self.bottom1box = gtk.HBox(False, 10)

		image = gtk.Image()
		image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
		image.set_pixel_size(10)
		self.topbox.pack_start(image, False, True, 5)
		image.show()
		label = gtk.Label("The following graphics hardware has been detected. \
Press 'Test Config' to see if it works. If you are satisfied with the \
result, click 'Yes' to save the new xorg.conf file. Otherwise, you can \
revise the selections and re-test until you have an optimal working \
configuration. Then click 'Close' and you're done.")
		label.set_line_wrap(True)
		self.topbox.pack_start(label, True, False, 0)
		label.show()

		self.leftgenbox = gtk.VBox(False, 0)
		self.rightgenbox = gtk.VBox(False, 0)
		label1 = gtk.Label("Graphics Card:")
		label1.set_line_wrap(True)
		label1.show()
		self.leftgenbox.pack_start(label1, True, False, 0)
		self.cardsel = gtk.combo_box_new_text()
		self.cardsel.show()
		self.rightgenbox.pack_start(self.cardsel, True, False, 0)
		label2 = gtk.Label("Graphics Driver:")
		label2.set_line_wrap(True)
		label2.show()
		self.leftgenbox.pack_start(label2, True, False, 0)
		self.driversel = gtk.combo_box_new_text()
		self.driversel.show()
		self.rightgenbox.pack_start(self.driversel, True, False, 0)
		label11 = gtk.Label("Video Memory:")
		label11.set_line_wrap(True)
		label11.show()
		self.leftgenbox.pack_start(label11, True, False, 0)
		self.graphicmem = gtk.Entry()
		self.graphicmem.show()
		self.rightgenbox.pack_start(self.graphicmem, True, False, 0)
		label8 = gtk.Label("Mouse Type:")
		label8.set_line_wrap(True)
		label8.show()
		self.leftgenbox.pack_start(label8, True, False, 0)
		self.mousesel = gtk.combo_box_new_text()
		self.mousesel.show()
		self.rightgenbox.pack_start(self.mousesel, True, False, 0)
		self.leftgenbox.show()
		self.rightgenbox.show()

		self.leftsimplebox = gtk.VBox(False, 0)
		self.rightsimplebox = gtk.VBox(False, 0)
		label3 = gtk.Label("Monitor Type:")
		label3.set_line_wrap(True)
		label3.show()
		self.leftsimplebox.pack_start(label3, True, False, 0)
		self.monitorsel = gtk.combo_box_new_text()
		self.monitorsel.show()
		self.rightsimplebox.pack_start(self.monitorsel, True, False, 0)
		label4 = gtk.Label("Resolution:")
		label4.set_line_wrap(True)
		label4.show()
		self.leftsimplebox.pack_start(label4, True, False, 0)
		self.ressel = gtk.combo_box_new_text()
		self.ressel.show()
		self.ressel.connect("changed", self.ResSelClick, None)
		self.rightsimplebox.pack_start(self.ressel, True, False, 0)
		label5 = gtk.Label("Colour Depth:")
		label5.set_line_wrap(True)
		label5.show()
		self.leftsimplebox.pack_start(label5, True, False, 0)
		self.depthsel = gtk.Entry()
		self.depthsel.show()
		self.rightsimplebox.pack_start(self.depthsel, True, False, 0)
		self.leftsimplebox.show()
		self.rightsimplebox.show()

		self.farleftexpertbox = gtk.VBox(False, 0)
		self.leftexpertbox = gtk.VBox(False, 0)
		self.centreexpertbox = gtk.VBox(False, 0)
		self.rightexpertbox = gtk.VBox(False, 0)
		self.farrightexpertbox = gtk.VBox(False, 0)
		self.lastexpertbox = gtk.VBox(False, 0)
		
		label4 = gtk.Label("Refresh Rate:")
		label4.set_line_wrap(True)
		self.farleftexpertbox.pack_start(label4, True, False, 0)
		self.refsel1 = gtk.Entry()
		self.refsel1.set_size_request(50, 30)
		self.leftexpertbox.pack_start(self.refsel1, True, False, 0)
		label5 = gtk.Label("to")
		label5.set_line_wrap(True)
		self.centreexpertbox.pack_start(label5, True, False, 0)
		self.refsel2 = gtk.Entry()
		self.refsel2.set_size_request(50, 30)
		self.rightexpertbox.pack_start(self.refsel2, True, False, 0)
		label9 = gtk.Label("Hz")
		label9.set_line_wrap(True)
		self.farrightexpertbox.pack_start(label9, True, False, 0)
		label4.show()
		self.refsel1.show()
		label5.show()
		self.refsel2.show()
		label9.show()
		
		label6 = gtk.Label("Horizontal Freq:")
		label6.set_line_wrap(True)
		self.farleftexpertbox.pack_start(label6, True, False, 0)
		self.hfreqsel1 = gtk.Entry()
		self.hfreqsel1.set_size_request(50, 30)
		self.leftexpertbox.pack_start(self.hfreqsel1, True, False, 0)
		label7 = gtk.Label("to")
		label7.set_line_wrap(True)
		self.centreexpertbox.pack_start(label7, True, False, 0)
		self.hfreqsel2 = gtk.Entry()
		self.hfreqsel2.set_size_request(50, 30)
		self.rightexpertbox.pack_start(self.hfreqsel2, True, False, 0)
		label10 = gtk.Label("kHz")
		label10.set_line_wrap(True)
		self.farrightexpertbox.pack_start(label10, True, False, 0)
		label6.show()
		self.hfreqsel1.show()
		label7.show()
		self.hfreqsel2.show()
		label10.show()
		
		self.button1 = gtk.Button("Test Config")
		self.button1.set_size_request(120, 30)
		self.button1.connect("clicked", self.TestConfig, None)
		self.button1.set_flags(gtk.CAN_DEFAULT)
		self.button1.show()
		self.bottom1box.pack_start(self.button1, True, False, 0)
		self.leftexpertbox.show()
		self.rightexpertbox.show()
		
		self.button7 = gtk.Button("Help")
		self.button7.set_size_request(120, 30)
		self.button7.connect("clicked", self.HelpClick, None)
		self.button7.set_flags(gtk.CAN_DEFAULT)
		self.button7.show()
		self.bottom1box.pack_start(self.button7, True, False, 0)
		self.leftexpertbox.show()
		self.rightexpertbox.show()
		self.button8 = gtk.Button("Close")
		self.button8.set_size_request(120, 30)
		self.button8.connect("clicked", self.close_application)
		self.button8.set_flags(gtk.CAN_DEFAULT)
		self.button8.show()
		self.bottom1box.pack_start(self.button8, True, False, 0)

		self.mainbox.pack_start(self.topbox, True, True, 0)
		self.topbox.show()
		self.separator = gtk.HSeparator()
		self.mainbox.pack_start(self.separator, True, True, 0)
		self.separator.show()
		self.genbox.pack_start(self.leftgenbox, True, False, 0)
		self.genbox.pack_start(self.rightgenbox, True, False, 0)
		self.genbox.show()
		self.simplebox.pack_start(self.leftsimplebox, True, False, 0)
		self.simplebox.pack_start(self.rightsimplebox, True, False, 0)
		self.simplebox.show()
		self.expertbox.pack_start(self.farleftexpertbox, True, False, 0)
		self.expertbox.pack_start(self.leftexpertbox, True, False, 0)
		self.expertbox.pack_start(self.centreexpertbox, True, False, 0)
		self.expertbox.pack_start(self.rightexpertbox, True, False, 0)
		self.expertbox.pack_start(self.farrightexpertbox, True, False, 0)
		self.expertbox.pack_start(self.lastexpertbox, True, False, 0)
		self.farleftexpertbox.show()
		self.leftexpertbox.show()
		self.centreexpertbox.show()
		self.rightexpertbox.show()
		self.farrightexpertbox.show()
		self.lastexpertbox.show()

		self.mainbox.pack_start(self.genbox, True, True, 0)
		self.separator = gtk.HSeparator()
		self.mainbox.pack_start(self.separator, True, True, 0)
		self.separator.show()
		self.mainbox.pack_start(self.simplebox, True, True, 0)
		self.separator = gtk.HSeparator()
		self.mainbox.pack_start(self.separator, True, True, 0)
		self.separator.show()
		self.mainbox.pack_start(self.expertbox, True, True, 0)
		self.expertbox.show()
		self.separator = gtk.HSeparator()
		self.mainbox.pack_start(self.separator, True, True, 0)
		self.separator.show()
		self.mainbox.pack_start(self.bottom1box, False, False, 5)
		self.bottom1box.show()

		self.InitValues(self, None)
		self.window.add(self.mainbox)
		self.mainbox.show()
		self.window.show()
		if (not self.found):
			self.ask_monitor(self, None)
		

