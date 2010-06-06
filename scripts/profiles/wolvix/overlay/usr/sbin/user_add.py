#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk, os, sys, pango, time, pwd, crypt

class UserAdd:

        def destroy_main(self, widget):
                self.window.destroy()        

        def create_click(self, widget):
            os.system('useradd -m -g %s -G %s -d %s -s %s -p "" %s' %(self.group_name.get_text(), 
		self.groups.get_text(), self.home_dir.get_text(), self.shell.get_text(), self.username))
	    os.system('xterm -e passwd %s' %self.username)
	    os.system("chown -R %s:%s %s" %(self.username, self.group_name.get_text(), self.home_dir.get_text())) 
	    message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
		"Addition of new user complete.")
	    resp = message.run()
	    message.destroy()
	    self.destroy_main(self)
	    return
	    
	def get_user_name(self):
	   user_window = gtk.Dialog("Host/Domain Name", None, gtk.DIALOG_MODAL, 
                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
           user_window.set_position(gtk.WIN_POS_CENTER)
           user_window.connect("destroy", self.destroy_main)
           user_window.set_title("Add New User")
           user_window.set_border_width(0)
           #self.window.set_size_request(360, 360)

           hbox1 = gtk.HBox(False, 0)
           image = gtk.Image()
           image.set_from_file("/usr/share/icons/Tango/scalable/apps/system-users.svg")
           hbox1.pack_start(image, False, False, 15)
           label1 = gtk.Label("Enter new user name:")
           label1.set_line_wrap(True)
           hbox1.pack_start(label1, False, False, 15)
           user_window.vbox.pack_start(hbox1, True, False, 10)
           
	   hbox2 = gtk.HBox(False, 0)
           user_name = gtk.Entry(15)
	   user_name.set_size_request(120, 25)
           hbox2.pack_start(user_name, True, False, 10)
           user_window.vbox.pack_start(hbox2, True, False, 15)
           user_window.show_all()
	   response = user_window.run()
           if (response == gtk.RESPONSE_ACCEPT):
                self.username = user_name.get_text()
	   user_window.destroy()
    	   return
	   
	def __init__(self):
           self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
           self.window.connect("destroy", self.destroy_main)
           self.window.set_title("Wolvix Add User")
           self.window.set_border_width(0)
           #self.window.set_size_request(360, 360)
   
           self.username = ""
	   self.get_user_name()
	   if self.username != "":
		vbox = gtk.VBox(False, 0)
		hbox1 = gtk.HBox(False, 0)
		image = gtk.Image()
		image.set_from_file("/usr/share/icons/Tango/scalable/apps/system-users.svg")
		hbox1.pack_start(image, False, False, 15)
		label1 = gtk.Label("Enter details for new user:")
		label1.set_line_wrap(True)
		hbox1.pack_start(label1, False, False, 15)
		vbox.pack_start(hbox1, True, False, 10)
		
		hbox3 = gtk.HBox(False, 0)
		label3 = gtk.Label("New user group:")
		label3.set_line_wrap(True)
		hbox3.pack_start(label3, True, False, 10)
		self.group_name = gtk.Entry(15)
		self.group_name.set_size_request(180, 25)
		self.group_name.set_text("users")
		hbox3.pack_start(self.group_name, True, False, 10)
		vbox.pack_start(hbox3, True, False, 5)
		
		hbox4 = gtk.HBox(False, 0)
		label4 = gtk.Label("Home directory:")
		label4.set_line_wrap(True)
		hbox4.pack_start(label4, True, False, 10)
		self.home_dir = gtk.Entry(15)
		self.home_dir.set_size_request(180, 25)
		self.home_dir.set_text("/home/%s" %self.username)
		hbox4.pack_start(self.home_dir, True, False, 10)
		vbox.pack_start(hbox4, True, False, 5)
		
		hbox5 = gtk.HBox(False, 0)
		label5 = gtk.Label("Shell:                ")
		label5.set_line_wrap(True)
		hbox5.pack_start(label5, True, False, 10)
		self.shell = gtk.Entry(15)
		self.shell.set_size_request(180, 25)
		self.shell.set_text("/bin/bash")
		hbox5.pack_start(self.shell, True, False, 10)
		vbox.pack_start(hbox5, True, False, 5)
		
		hbox6 = gtk.HBox(False, 0)
		label6 = gtk.Label("Extra groups:    ")
		label6.set_line_wrap(True)
		hbox6.pack_start(label6, True, False, 10)
		self.groups = gtk.Entry(100)
		self.groups.set_size_request(180, 25)
		self.groups.set_text("users,floppy,audio,optical,storage,disk,video,games,power,scanner,hal,dbus,vboxusers")
		hbox6.pack_start(self.groups, True, False, 10)
		vbox.pack_start(hbox6, True, False, 5)
		
		separator = gtk.HSeparator()
		vbox.pack_start(separator, True, False, 10)
		
		hbox4 = gtk.HBox(False, 0)
		button = gtk.Button("Create")
		button.set_size_request(100, 30)
		button.connect_object("clicked", self.create_click, self.window)
		hbox4.pack_start( button, True, False, 0)
		button = gtk.Button("Done")
		button.set_size_request(100, 30)
		button.connect_object("clicked", self.destroy_main, self.window)
		#button.set_flags(gtk.CAN_DEFAULT)
		hbox4.pack_start( button, True, False, 0)
		vbox.pack_start(hbox4, True, False, 10)
		self.window.add(vbox)
		self.window.show_all()
		
