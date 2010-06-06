#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk, os, sys

class DevFormat:
        def destroy_main(self, widget):
           self.window.destroy()
   
        def format_click(self, data = None):
            selection = self.listControl.get_selection()
            (model, iter) = selection.get_selected()
            id = model.get_value(iter, 0)
            self.mountpoint = "/mnt/" + id[5:]
	    os.system("mount > /tmp/mount.txt")
	    for line in file('/tmp/mount.txt').readlines():
		word = line.split(None, sys.maxint)
		index = word.count(id)
		#print ("Index = %s; line = %s" %(index, line))
		if (index>=1):
			#print ("Index = %s; Device = %s" %(index, id))
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
				"Device %s is mounted on %s.\n\
Cannot format mounted device.\nPlease unmount and try again.\n" % (id, self.mountpoint)) 
			resp = message.run()
			message.destroy()
			return
	    message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, 
		"About to format %s.\nAll data will be destroyed.\n\
Continue? (Y/N)" % id) 
	    resp = message.run()
	    message.destroy()
            if (resp== gtk.RESPONSE_NO):
		return
	    if ((self.fssel.get_active_text()=="xfs") or (self.fssel.get_active_text()=="reiserfs")):
		self.fs = self.fssel.get_active_text() + " -f"
		os.system("mkfs -t %s %s" % (self.fs, id))
	    elif((self.fssel.get_active_text()=="ext2") or (self.fssel.get_active_text()=="ext3")):
		self.fs = self.fssel.get_active_text()
		os.system("mkfs -t %s %s" % (self.fs, id))
	    else:
		os.system("mkdosfs -F 32 %s" %id)
	    fs_txt = self.fssel.get_active_text()
	    message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
				"Format of device %s complete" % id) 
	    resp = message.run()
	    message.destroy()
	    self.destroy_main(self)
			
	def get_devices(self, widget):
		os.system("fdisk -l >/tmp/fdisk.txt")
		file = open('/tmp/fdisk.txt')
		fdisk = file.read()
		file.close()
		lines = fdisk.split("\n", sys.maxint)
		for line in lines:
			index = line.find("/dev/", 0, sys.maxint)
			if ((index >= 0) and (line.find("swap", 0, sys.maxint)<0) and 
				(line.find("Disk", 0, sys.maxint)<0) and (line.find("Extended", 0, sys.maxint)<0)):
				word = line.split(None, sys.maxint)
				self.device_list.append(word[0].split('\n'))
	    
        def make_listbox(self, widget):
           self.store.clear()
           self.column1.clear()
           self.column2.clear()
           # Get user info
           self.device_list = []
           self.get_devices(None)
	   for device in self.device_list:
                self.store.append([device[0], ""])
           renderer1 = gtk.CellRendererText()
           self.column1.pack_start(renderer1)
           self.column1.set_attributes(renderer1, text = 0)
           renderer2 = gtk.CellRendererText()
           self.column2.pack_start(renderer2)
           self.column2.set_attributes(renderer2, text = 1)
            
        def __init__(self):
           self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
           self.window.connect("destroy", self.destroy_main)
           self.window.set_title("Wolvix Device Format")
           self.window.set_border_width(0)
           #self.window.set_size_request(360, 360)
   
           vbox = gtk.VBox(False, 0)
	   hbox1 = gtk.HBox(False, 0)
	   image = gtk.Image()
	   image.set_from_file("/usr/share/icons/Tango/scalable/devices/drive-format.svg")
	   hbox1.pack_start(image, False, False, 15)
	   label1 = gtk.Label("Select device to format:")
	   label1.set_line_wrap(True)
	   hbox1.pack_start(label1, False, False, 15)
	   vbox.pack_start(hbox1, True, False, 10)
		
	   scrolled_window = gtk.ScrolledWindow()
           scrolled_window.set_border_width(10)
           scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
           scrolled_window.set_size_request(320, 240)
           vbox.pack_start(scrolled_window, True, True, 0)
        
           label2 = gtk.Label("Select filesystem for device format:")
	   label2.set_line_wrap(True)
	   vbox.pack_start(label2, True, False, 0)
	   label2.show()
	   self.fssel = gtk.combo_box_new_text()
	   self.fssel.set_size_request(100, 30)
	   self.fssel.append_text("ext2")
	   self.fssel.append_text("ext3")
	   self.fssel.append_text("reiserfs")
	   self.fssel.append_text("xfs")
	   self.fssel.append_text("fat32")
	   self.fssel.set_active(1)
	   vbox.pack_start(self.fssel, True, False, 10)
	   self.fssel.show()   
	   
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
           vbox.pack_start(hbox2, True, False, 10)
           button = gtk.Button("Format")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.format_click, self.window)
           hbox2.pack_start( button, True, False, 10)
           button = gtk.Button("Done")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.destroy_main, self.window)
           #button.set_flags(gtk.CAN_DEFAULT)
           hbox2.pack_start( button, True, False, 10)
           #self.listControl.connect('row-activated', self.rowActivated)
           self.window.add(vbox)
           self.window.show_all()