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

class WirelessConfig:

    def HelpClick(self, widget, data=None):

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
        textbuffer.set_text("Wolvix Wireless Config")
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
        
    def close_application(self, widget, data=None):
        self.window.destroy()

    def get_interfaces(self, widget, data=None):
	os.system("iwconfig > /tmp/iface.txt")
	for line in file('/tmp/iface.txt').readlines():
            if line.count("eth", 0, sys.maxint) or line.count("wlan") and not line.count("no wireless"):
                 word = line.split(None, sys.maxint)
                 print "Found device %s\n" %word[0]
		 self.cardsel.append_text(word[0])
	self.cardsel.set_active(0)

    def connect(self, widget, data=None):
	iface = self.cardsel.get_active_text()
        os.system("ifconfig %s down" %iface)
	essid = self.entry1.get_text()
	os.system("iwconfig %s essid %s" %(iface, essid))
	secure = self.securesel.get_active_text()
	key = self.entry2.get_text()
	os.system("iwconfig %s key %s %s" %(iface, secure, key))
	channel = self.chansel.get_active_text()
	os.system("iwconfig %s channel %s" %(iface, channel))
	rate = "auto"
	os.system("iwconfig %s rate %s" %(iface, rate))
	mode = self.modesel.get_active_text()
	os.system("iwconfig %s mode %s" %(iface, mode))
        os.system("ifconfig %s up" %iface)
	
	message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                "Wireless network connected.")
	resp = message.run()
        message.destroy()
	self.window.destroy()
    
    def dhcpClick(self, widget, data=None):
        if self.dhcpsel.get_active_text()=="no":	
		self.label7.show()
		self.entry3.show()
		self.label8.show()
		self.entry4.show()
		self.label9.show()
		self.entry5.show()
		self.label10.show()
		self.entry6.show()
		self.label11.show()
		self.entry7.show()
		self.label12.show()
		self.entry8.show()
	else:
		self.window.destroy()
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#self.window.set_size_request(380, 380)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_resizable(True)

		self.window.connect("destroy", self.close_application)
		self.window.set_title("Wolvix Wireless Config")
		self.window.set_border_width(10)

		self.mainbox = gtk.VBox(False, 10)
		self.populate(self, None)
		self.label7.hide()
		self.entry3.hide()
		self.label8.hide()
		self.entry4.hide()
		self.label9.hide()
		self.entry5.hide()
		self.label10.hide()
		self.entry6.hide()
		self.label11.hide()
		self.entry7.hide()
		self.label12.hide()
		self.entry8.hide()
		self.window.add(self.mainbox)
		self.mainbox.show()         
		self.window.show()

	return
    
    def populate(self, widget, data=None):
	self.topbox = gtk.HBox(False, 10)
        self.centrebox = gtk.VBox(False, 10)
        self.leftbox = gtk.VBox(False, 10)
        self.rightbox = gtk.VBox(False, 10)
        image = gtk.Image()
        image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
        self.rightbox.pack_start(image, False, False, 10)
        image.show()
               
        label0 = gtk.Label("Interface:")
        label0.set_line_wrap(True)
        self.cardsel = gtk.combo_box_new_text()
        self.cardsel.set_size_request(180, 30)
	self.get_interfaces(self, None)
	label1 = gtk.Label("Network Name:")
        label1.set_line_wrap(True)
        self.entry1 = gtk.Entry(36)
	self.entry1.set_text("essid")
        self.entry1.set_size_request(180, 30)
        label2 = gtk.Label("Mode:")
        label2.set_line_wrap(True)
        self.modesel = gtk.combo_box_new_text()
        self.modesel.set_size_request(180, 30)
	for mode in ["auto", "Managed", "Ad-Hoc", "Master", "Repeater", "Secondary", "Monitor"]:
            self.modesel.append_text(mode)
	self.modesel.set_active(0)
	label3 = gtk.Label("Channel:")
        label3.set_line_wrap(True)
        self.chansel = gtk.combo_box_new_text()
        self.chansel.set_size_request(180, 30)
	for channel in ["auto", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]:
            self.chansel.append_text(channel)
	self.chansel.set_active(0)
	label4 = gtk.Label("Security:")
        label4.set_line_wrap(True)
        self.securesel = gtk.combo_box_new_text()
        self.securesel.set_size_request(180, 30)
	for state in ["open", "restricted"]:
            self.securesel.append_text(state)
	self.securesel.set_active(0)
	label5 = gtk.Label("Key:")
        label5.set_line_wrap(True)
        self.entry2 = gtk.Entry(36)
	self.entry2.set_text("")
        self.entry2.set_size_request(180, 30)
        label6 = gtk.Label("Use DHCP:")
        label6.set_line_wrap(True)
        self.dhcpsel = gtk.combo_box_new_text()
        self.dhcpsel.set_size_request(180, 30)
	for state in ["yes", "no"]:
           self.dhcpsel.append_text(state)
	self.dhcpsel.set_active(0)
	self.label7 = gtk.Label("IP Address:")
        self.label7.set_line_wrap(True)
        self.entry3 = gtk.Entry(36)
	self.entry3.set_text("")
        self.entry3.set_size_request(180, 30)
        self.label8 = gtk.Label("Netmask:")
        self.label8.set_line_wrap(True)
        self.entry4 = gtk.Entry(36)
	self.entry4.set_text("")
        self.entry4.set_size_request(180, 30)
        self.label9 = gtk.Label("Gateway:")
        self.label9.set_line_wrap(True)
        self.entry5 = gtk.Entry(36)
	self.entry5.set_text("")
        self.entry5.set_size_request(180, 30)
        self.label10 = gtk.Label("Domain:")
        self.label10.set_line_wrap(True)
        self.entry6 = gtk.Entry(36)
	self.entry6.set_text("")
        self.entry6.set_size_request(180, 30)
        self.label11 = gtk.Label("DNS:")
        self.label11.set_line_wrap(True)
        self.entry7 = gtk.Entry(36)
	self.entry7.set_text("")
        self.entry7.set_size_request(180, 30)
        self.label12 = gtk.Label("DNS:")
        self.label12.set_line_wrap(True)
        self.entry8 = gtk.Entry(36)
	self.entry8.set_text("")
        self.entry8.set_size_request(180, 30)
        
	self.leftbox.pack_start(label0, True, False, 0)
        self.centrebox.pack_start(self.cardsel, True, False, 0)
        self.leftbox.pack_start(label1, True, False, 0)
        self.centrebox.pack_start(self.entry1, True, False, 0)
        self.leftbox.pack_start(label2, True, False, 0)
        self.centrebox.pack_start(self.modesel, True, False, 0)
        self.leftbox.pack_start(label3, True, False, 0)
        self.centrebox.pack_start(self.chansel, True, False, 0)
        self.leftbox.pack_start(label4, True, False, 0)
        self.centrebox.pack_start(self.securesel, True, False, 0)
        self.leftbox.pack_start(label5, True, False, 0)
        self.centrebox.pack_start(self.entry2, True, False, 0)
        self.leftbox.pack_start(label6, True, False, 0)
        self.centrebox.pack_start(self.dhcpsel, True, False, 0)
        self.dhcpsel.connect("changed", self.dhcpClick, None)
        self.leftbox.pack_start(self.label7, True, False, 0)
        self.centrebox.pack_start(self.entry3, True, False, 0)
        self.leftbox.pack_start(self.label8, True, False, 0)
        self.centrebox.pack_start(self.entry4, True, False, 0)
        self.leftbox.pack_start(self.label9, True, False, 0)
        self.centrebox.pack_start(self.entry5, True, False, 0)
        self.leftbox.pack_start(self.label10, True, False, 0)
        self.centrebox.pack_start(self.entry6, True, False, 0)
        self.leftbox.pack_start(self.label11, True, False, 0)
        self.centrebox.pack_start(self.entry7, True, False, 0)
        self.leftbox.pack_start(self.label12, True, False, 0)
        self.centrebox.pack_start(self.entry8, True, False, 0)
        
	label0.show()
        label1.show()
        label2.show()
	label3.show()
        label4.show()
	label5.show()
        label6.show()
        self.cardsel.show()
        self.entry1.show()
        self.modesel.show()
        self.chansel.show()
        self.securesel.show()
        self.entry2.show()
        self.dhcpsel.show()
        
        self.topbox.pack_start(self.leftbox, True, False, 10)
        self.topbox.pack_start(self.centrebox, True, False, 10)
        self.topbox.pack_start(self.rightbox, True, False, 10)
        self.leftbox.show()
        self.centrebox.show()
        self.rightbox.show()
        
        self.bottombox = gtk.HBox(False, 10)
        self.button6 = gtk.Button("Help")
        self.button6.set_size_request(120, 30)
        self.button6.connect("clicked", self.HelpClick)
        self.bottombox.pack_start(self.button6, True, False, 10)
        self.button6.show()	
        self.button5 = gtk.Button("Connect")
        self.button5.set_size_request(120, 30)
        self.button5.connect("clicked", self.connect)
        self.bottombox.pack_start(self.button5, True, False, 10)
        self.button5.show()	
        self.button8 = gtk.Button("Close")
        self.button8.set_size_request(120, 30)
        self.button8.connect("clicked", self.close_application)
        self.button8.set_flags(gtk.CAN_DEFAULT)
        self.bottombox.pack_start(self.button8, True, False, 10)
        self.button8.show()

        self.mainbox.pack_start(self.topbox, True, True, 0)
        self.topbox.show()
        self.separator = gtk.HSeparator()
	self.mainbox.pack_start(self.separator, False, True, 5)
	self.separator.show()
	self.mainbox.pack_start(self.bottombox, False, False, 5)
        self.bottombox.show()
        
    def __init__(self):
        gtk.rc_parse("/etc/gtk/gtkrc.iso-8859-2")
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.window.set_size_request(380, 380)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_resizable(True)

        self.window.connect("destroy", self.close_application)
        self.window.set_title("Wolvix Wireless Config")
        self.window.set_border_width(10)

        self.mainbox = gtk.VBox(False, 10)
        self.populate(self, None)
	self.window.add(self.mainbox)
        self.mainbox.show()         
        self.window.show()

        