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
from ftplib import FTP

from mkbootloader import *

class KernelCompile:

	def close_application(self, widget, data=None):
		self.window.destroy()

	def TextBufferChange(self, widget, data=None):
		self.textview.scroll_to_iter(self.textbuffer.get_end_iter(), 0.1, True, 0.5, 0.5)

	def get_kernel_env(self, widget, data=None):
		return
		
	def get_src(self, widget):
		selection = self.listControl.get_selection()
		(model, iter) = selection.get_selected()
		self.id = model.get_value(iter, 0)
		self.kernel_name = ""
		self.get_kernel_name(self, None)
		os.system("mkdir /usr/src/%s" %self.kernel_name)
		os.system("rm /usr/src/linux")
		os.system("ln -s /usr/src/%s /usr/src/linux" %self.kernel_name)
		os.system('touch /tmp/run')
		os.system("/usr/sbin/restart_status.py & wget -r --no-host-directories --directory-prefix=/usr/src/linux ftp://ftp.wolvix.org/wolvix/development/wolven/kernel/*")
	        os.system('rm /tmp/run')
		os.system('cp -ar /usr/src/linux/wolvix/development/wolven/kernel/* /usr/src/linux')
		os.system('rm -rf /usr/src/linux/wolvix')
		os.system('mv /usr/src/linux/config /usr/src/linux/.config')
		
		print "Getting ftp://ftp.kernel.org/pub/linux/kernel/v2.6/%s" %self.id
		os.system('touch /tmp/run')
		os.system("/usr/sbin/restart_status.py & wget --directory-prefix=/usr/src/linux ftp://ftp.kernel.org/pub/linux/kernel/v2.6/%s" %self.id)
		os.system('rm /tmp/run')
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
			"Wolvix kernel environment and kernel source downloaded.")
		resp = message.run()
		message.destroy()
		self.destroy_list(None)
		
	def destroy_list(self, widget, data=None):
		self.list_window.destroy()
	
	def destroy_getname(self, widget):
		self.name_window.destroy()
	
	def get_kernel_name(self, widget, data=None):
		name_window = gtk.Dialog("Host/Domain Name", None, gtk.DIALOG_MODAL, 
			(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		name_window.set_position(gtk.WIN_POS_CENTER)
		name_window.connect("destroy", self.destroy_getname)
		name_window.set_title("Get unique kernel identifier")
		name_window.set_border_width(0)
		#self.window.set_size_request(360, 360)

		hbox1 = gtk.HBox(False, 0)
		image = gtk.Image()
		image.set_from_file("/usr/share/icons/Tango/scalable/apps/system-users.svg")
		hbox1.pack_start(image, False, False, 15)
		label1 = gtk.Label("Modify for unique kernel identifier:")
		label1.set_line_wrap(True)
		hbox1.pack_start(label1, False, False, 15)
		name_window.vbox.pack_start(hbox1, True, False, 10)
           
		hbox2 = gtk.HBox(False, 0)
		kernel_name = gtk.Entry(32)
		name = self.id.split('.tar', sys.maxint)
		kernel_name.set_text(name[0])
		kernel_name.set_size_request(180, 25)
		hbox2.pack_start(kernel_name, True, False, 10)
		name_window.vbox.pack_start(hbox2, True, False, 15)
		name_window.show_all()
		response = name_window.run()
		if (response == gtk.RESPONSE_ACCEPT):
			self.kernel_name = kernel_name.get_text()
		name_window.destroy()
		return
	   
	def destroy_list(self, widget):
	    self.list_window.destroy()
		
	def make_listbox(self, widget):
		ftp =FTP("ftp.kernel.org")
		ftp.login("ftp", "ftp")
		ftp.cwd("pub/linux/kernel/v2.6")
		self.filelist=[]
		ftp.retrlines("LIST linux*.bz2", self.filelist.append)
		ftp.quit()
		self.store.clear()
		self.column1.clear()
		self.column2.clear()
		# Get user info
		for line in self.filelist:
			word=line.split(None, sys.maxint)
			self.store.append([word[8], ""])
		renderer1 = gtk.CellRendererText()
		self.column1.pack_start(renderer1)
		self.column1.set_attributes(renderer1, text = 0)
		renderer2 = gtk.CellRendererText()
		self.column2.pack_start(renderer2)
		self.column2.set_attributes(renderer2, text = 1)
            
	def get_source(self, widget, data=None):
		self.list_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.list_window.connect("destroy", self.destroy_list)
		self.list_window.set_title("Download kernel source")
		self.list_window.set_border_width(0)
		#self.list_window.set_size_request(360, 360)
   
		vbox = gtk.VBox(False, 0)
		hbox1 = gtk.HBox(False, 0)
		image = gtk.Image()
		image.set_from_file("/usr/share/icons/Wolvix/tango/module.svg")
		hbox1.pack_start(image, False, False, 15)
		label1 = gtk.Label("Select kernel to download and click 'OK'.")
		label1.set_line_wrap(True)
		hbox1.pack_start(label1, False, False, 15)
		vbox.pack_start(hbox1, True, False, 10)
		
		scrolled_window = gtk.ScrolledWindow()
		scrolled_window.set_border_width(10)
		scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		scrolled_window.set_size_request(360, 240)
		vbox.pack_start(scrolled_window, True, True, 0)
        	table = gtk.Table(1, 1, False)
		scrolled_window.add_with_viewport(table)
		self.store = gtk.ListStore(str, str)
		self.listControl = gtk.TreeView(self.store)
		self.column1 = gtk.TreeViewColumn("")
		self.column2 = gtk.TreeViewColumn("")
		self.listControl.append_column(self.column1)	   
		self.listControl.append_column(self.column2)	   
		self.make_listbox(self)
		table.attach(self.listControl, 0, 1, 0, 1)
		hbox2 = gtk.HBox(False, 0)
		vbox.pack_start(hbox2, True, False, 0)
		button = gtk.Button("Get")
		button.set_size_request(100, 30)
		button.connect_object("clicked", self.get_src, self.list_window)
		hbox2.pack_start( button, True, False, 0)
		button = gtk.Button("Done")
		button.set_size_request(100, 30)
		button.connect_object("clicked", self.destroy_list, self.list_window)
		hbox2.pack_start( button, True, False, 0)
		#self.listControl.connect('row-activated', self.rowActivated)
		self.list_window.add(vbox)
		self.list_window.show_all()
		return True
	        
	def run_config(self, widget, data=None):
		return
		
	def select_patches(self, widget, data=None):
		return
		
	def __init__(self):
		gtk.rc_parse("/etc/gtk/gtkrc.iso-8859-2")
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#self.window.set_size_request(560, 560)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_resizable(True)

		self.window.connect("destroy", self.close_application)
		self.window.set_title("Wolvix Kernel Compiler")
		self.window.set_border_width(10)

		self.mainbox = gtk.VBox(False, 0)
		self.topbox = gtk.HBox(False, 0)

		self.leftbox = gtk.VBox(False, 5)
		image = gtk.Image()
		image.set_from_file("/usr/share/pixmaps/wolvix-menu.png")
		self.leftbox.pack_start(image, True, False, 5)
		image.show()

		self.centrebox = gtk.VBox(False, 10)
		label1 = gtk.Label("                                                        1: Download kernel source:  ")
		label1.set_line_wrap(True)
		self.centrebox.pack_start(label1, True, False, 0)
		label1.show()
		label2 = gtk.Label("                                                      2: Run kernel configuration:")
		label2.set_line_wrap(True)
		self.centrebox.pack_start(label2, True, False, 0)
		label2.show()
		label3 = gtk.Label("                                                      3: Select kernel patches:   ")
		label3.set_line_wrap(True)
		self.centrebox.pack_start(label3, True, False, 0)
		label3.show()
		
		self.rightbox = gtk.VBox(False, 10)
		self.button1 = gtk.Button("Get Source")
		self.button1.set_size_request(80, 30)
		self.button1.connect_object("clicked", self.get_source, self.window, None)
		self.rightbox.pack_start(self.button1, True, False, 0)
		self.button1.show()
		self.button2 = gtk.Button("Run Config")
		self.button2.set_size_request(80, 30)
		self.button2.connect_object("clicked", self.run_config, self.window, None)
		self.rightbox.pack_start(self.button2, True, False, 0)
		self.button2.show()
		self.button3 = gtk.Button("Patches")
		self.button3.set_size_request(80, 30)
		self.button3.connect_object("clicked", self.select_patches, self.window, None)
		self.rightbox.pack_start(self.button3, True, False, 0)
		self.button3.show()

		self.middlebox = gtk.HBox(False, 10)
		self.sw = gtk.ScrolledWindow()
		self.sw.set_shadow_type(gtk.SHADOW_IN)
		self.sw.set_size_request(740, 300)
		self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.textview = gtk.TextView()
		self.textview.set_wrap_mode(gtk.WRAP_WORD)
		self.textbuffer = gtk.TextBuffer()
		self.textbuffer.set_text(" This utility is in development...Use with care!\n\n\
 This compilation log will be saved to /var/log/compiler.log \
after the compile process completes. If you have a problem, \
read this file as a first step to finding what went wrong.\n\n\
 You must perform the following steps to use this utility:\n\
 1: Download the source for the kernel you wish to compile.\n\
 2: Run the config utility - you may modify the standard \
Wolvix config if you wish..\n\
 3: Select kernel patches - you may select/deselect Wolvix \
standard patches, or your own patch files.\n\
 4: Start the compile process - this will take some time, \
progress will be indicated by the compiler output in this \
window.\n\n")
		self.textbuffer.connect("changed", self.TextBufferChange, None)
		self.textview.set_buffer(self.textbuffer)
		self.sw.add(self.textview)
		self.middlebox.pack_start(self.sw, True, True, 10)
		self.sw.show()
		self.textview.show()
		
		self.bottombox = gtk.HBox(False, 10)
		self.button7 = gtk.Button("4: Start")
		self.button7.set_size_request(110, 30)
		self.button7.connect_object("clicked", self.get_kernel_env, self.window, None)
		self.button7.set_flags(gtk.CAN_DEFAULT)
		self.bottombox.pack_start(self.button7, True, False, 10)
		self.button7.show()
		self.button8 = gtk.Button("Close")
		self.button8.set_size_request(110, 30)
		self.button8.connect("clicked", self.close_application)
		self.button8.set_flags(gtk.CAN_DEFAULT)
		self.bottombox.pack_start(self.button8, True, False, 10)
		self.button8.show()

		self.topbox.pack_start(self.leftbox, False, False, 10)
		self.topbox.pack_start(self.centrebox, False, False, 10)
		self.topbox.pack_end(self.rightbox, True, True, 10)
		self.leftbox.show()
		self.centrebox.show()
		self.rightbox.show()
		
		self.mainbox.pack_start(self.topbox, True, True, 0)
		self.topbox.show()
		self.mainbox.pack_start(self.middlebox, True, True, 10)
		self.middlebox.show()
		self.mainbox.pack_start(self.bottombox,True, False, 0)
		self.bottombox.show()

		self.window.add(self.mainbox)
		self.mainbox.show()
		self.window.show()

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
