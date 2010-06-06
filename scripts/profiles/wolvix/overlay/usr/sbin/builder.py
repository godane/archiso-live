#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk, os, sys

class WolvixBuilder:
        def destroy_main(self, widget):
           self.window.destroy()
   
        def delete_click(self, data = None):
            selection = self.listControl.get_selection()
            (model, iter) = selection.get_selected()
            id = model.get_value(iter, 0)
            os.system("userdel -r %s" %id)
            self.make_listbox(self)
            self.window.show_all()

	def get_users(self, widget):
            # getting current DNS parameters
            info = ""
            os.system("cat /etc/passwd > /tmp/userinfo.txt")
            for line in file('/tmp/userinfo.txt').readlines():
                word = line.split(":")
		if int(word[2])>999:
                    self.user_list.append(word[0].split('\n'))
	    
        def make_listbox(self, widget):
           self.store.clear()
           self.column1.clear()
           self.column2.clear()
           # Get user info
           self.user_list = []
           self.get_users(None)
	   print ("%s\n" %self.user_list)
           for user in self.user_list:
                self.store.append([user[0], ""])
           renderer1 = gtk.CellRendererText()
           self.column1.pack_start(renderer1)
           self.column1.set_attributes(renderer1, text = 0)
           renderer2 = gtk.CellRendererText()
           self.column2.pack_start(renderer2)
           self.column2.set_attributes(renderer2, text = 1)
            
        def __init__(self):
           self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
           self.window.connect("destroy", self.destroy_main)
           self.window.set_title("Wolvix Builder")
           self.window.set_border_width(0)
           #self.window.set_size_request(360, 360)
   
           vbox = gtk.VBox(False, 0)
	   title_hbox = gtk.HBox(False, 0)
	   label1 = gtk.Label("SOURCE DIR:")
	   title_hbox.pack_start(label1, False, False, 10)
	   image = gtk.Image()
	   image.set_from_file("/usr/share/icons/Tango/scalable/stock/go-next.svg")
	   hbox1.pack_start(image, False, False, 10)
	   label2 = gtk.Label("Welcome to Wolvix Builder - Version 0.2")
	   title_hbox.pack_start(label2, False, False, 15)
	   image = gtk.Image()
	   image.set_from_file("/usr/share/icons/Tango/scalable/stock/go-next.svg")
	   title_hbox.pack_start(image, False, False, 10)
	   label3 = gtk.Label("DESTINATION DIR:")
	   title_hbox.pack_start(label3, False, False, 10)
	   vbox.pack_start(title_hbox, True, True, 0)
        	
	   scrolled_window = gtk.ScrolledWindow()
           scrolled_window.set_border_width(10)
           scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
           scrolled_window.set_size_request(320, 240)
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
           button = gtk.Button("Delete")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.delete_click, self.window)
           hbox2.pack_start( button, True, False, 0)
           button = gtk.Button("Done")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.destroy_main, self.window)
           #button.set_flags(gtk.CAN_DEFAULT)
           hbox2.pack_start( button, True, False, 0)
           #self.listControl.connect('row-activated', self.rowActivated)
           self.window.add(vbox)
           self.window.show_all()