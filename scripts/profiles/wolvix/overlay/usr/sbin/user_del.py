#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk, os, sys

class UserDel:
        def destroy_main(self, widget):
           self.window.destroy()
   
        def delete_click(self, data = None):
            selection = self.listControl.get_selection()
            (model, iter) = selection.get_selected()
            id = model.get_value(iter, 0)
            message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE,
                "Warning. The user %s, the associated home directory and all the data files \
therein are about to be destroyed. Continue?" %id)
	    message.add_button(gtk.STOCK_YES, gtk.RESPONSE_ACCEPT)
            message.add_button(gtk.STOCK_NO, gtk.RESPONSE_REJECT)
            resp = message.run()
	    message.destroy()
	    if (resp == gtk.RESPONSE_REJECT):
		return
	
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
           self.window.set_title("Wolvix Delete User")
           self.window.set_border_width(0)
           #self.window.set_size_request(360, 360)
   
           vbox = gtk.VBox(False, 0)
	   hbox1 = gtk.HBox(False, 0)
	   image = gtk.Image()
	   image.set_from_file("/usr/share/icons/Tango/scalable/stock/removeuser.svg")
	   hbox1.pack_start(image, False, False, 15)
	   label1 = gtk.Label("Select user to delete:")
	   label1.set_line_wrap(True)
	   hbox1.pack_start(label1, False, False, 15)
	   vbox.pack_start(hbox1, True, False, 10)
		
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