#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk, os, sys, time

class DateTime:
        def destroy_main(self, widget):
           self.window.destroy()
            
        def set_click(self, widget):
           day = int(self.spinner1.get_value())
	   if (day>9):
		day_str = str(day)
	   else:
		day_str = "0" + str(day)
	   month = int(self.spinner2.get_value())
	   if (month>9):
		month_str = str(month)
	   else:
		month_str = "0" + str(month)
	   year = int(self.spinner3.get_value())
	   if (year>9):
		year_str = str(year)
	   else:
		year_str = "0" + str(year)
	   hour = int(self.spinner4.get_value())
	   if (hour>9):
		hour_str = str(hour)
	   else:
		hour_str = "0" + str(hour)
	   mins = int(self.spinner5.get_value())
	   if (mins>9):
		mins_str = str(mins)
	   else:
		mins_str = "0" + str(mins)
	   secs = int(self.spinner6.get_value())
	   if (secs>9):
		secs_str = str(secs)
	   else:
		secs_str = "0" + str(secs)
	   os.system("date %s%s%s%s%s.%s" %(month_str, day_str, hour_str, mins_str, year_str, secs_str))
	   return
        
	def __init__(self):
           self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
           self.window.connect("destroy", self.destroy_main)
           self.window.set_title("Wolvix Set Date & Time")
           self.window.set_border_width(0)
           #self.window.set_size_request(360, 360)
   
           vbox = gtk.VBox(False, 0)
	   hbox1 = gtk.HBox(False, 0)
	   image = gtk.Image()
	   image.set_from_file("/usr/share/icons/Tango/scalable/apps/date.svg")
	   hbox1.pack_start(image, False, False, 15)
	   label1 = gtk.Label("Adjust date and time and click 'OK':")
	   label1.set_line_wrap(True)
	   hbox1.pack_start(label1, False, False, 15)
	   vbox.pack_start(hbox1, True, False, 10)
	   
	   current_time = time.gmtime(time.time())
	   
	   hbox2 = gtk.HBox(False, 0)
	   
	   vbox2 = gtk.VBox(False, 0)
	   hbox2.pack_start(vbox2, True, True, 5)
           label = gtk.Label("Day :")
           label.set_alignment(0, 0.5)
           vbox2.pack_start(label, False, True, 0)
	   current_day = current_time[2]
           self.adj1 = gtk.Adjustment(current_day, 1.0, 31.0, 1.0, 5.0, 0.0)  # initial, lwr, uppr, step, page inc, page size
           self.spinner1 = gtk.SpinButton(self.adj1, 0, 0)
           self.spinner1.set_wrap(True)
           vbox2.pack_start(self.spinner1, False, True, 0)
  
	   vbox2 = gtk.VBox(False, 0)
	   hbox2.pack_start(vbox2, True, True, 5)
           label = gtk.Label("Month :")
           label.set_alignment(0, 0.5)
           vbox2.pack_start(label, False, True, 0)
           current_month = current_time[1]
           self.adj2 = gtk.Adjustment(current_month, 1.0, 12.0, 1.0, 5.0, 0.0)
           self.spinner2 = gtk.SpinButton(self.adj2, 0, 0)
           self.spinner2.set_wrap(True)
           vbox2.pack_start(self.spinner2, False, True, 0)
	   
           vbox2 = gtk.VBox(False, 0)
	   hbox2.pack_start(vbox2, True, True, 5)
           label = gtk.Label("Year :")
           label.set_alignment(0, 0.5)
           vbox2.pack_start(label, False, True, 0)
           current_year = current_time[0]
	   self.adj3 = gtk.Adjustment(current_year, 2000.0, 2020.0, 1.0, 5.0, 0.0)
           self.spinner3 = gtk.SpinButton(self.adj3, 0, 0)
           self.spinner3.set_wrap(True)
           vbox2.pack_start(self.spinner3, False, True, 0)
	   
	   vbox2 = gtk.VBox(False, 0)
	   hbox2.pack_start(vbox2, True, True, 5)
           label = gtk.Label("Hour :")
           label.set_alignment(0, 0.5)
           vbox2.pack_start(label, False, True, 0)
           current_hour = current_time[3]
	   self.adj4 = gtk.Adjustment(current_hour, 0.0, 23.0, 1.0, 5.0, 0.0)
           self.spinner4 = gtk.SpinButton(self.adj4, 0, 0)
           self.spinner4.set_wrap(True)
           vbox2.pack_start(self.spinner4, False, True, 0)
	   
	   vbox2 = gtk.VBox(False, 0)
	   hbox2.pack_start(vbox2, True, True, 5)
           label = gtk.Label("Minute :")
           label.set_alignment(0, 0.5)
           vbox2.pack_start(label, False, True, 0)
           current_min = current_time[4]
	   self.adj5 = gtk.Adjustment(current_min, 0.0, 59.0, 1.0, 5.0, 0.0)
           self.spinner5 = gtk.SpinButton(self.adj5, 0, 0)
           self.spinner5.set_wrap(True)
           vbox2.pack_start(self.spinner5, False, True, 0)
	   
	   vbox2 = gtk.VBox(False, 0)
	   hbox2.pack_start(vbox2, True, True, 5)
           label = gtk.Label("Sec :")
           label.set_alignment(0, 0.5)
           vbox2.pack_start(label, False, True, 0)
           current_sec = current_time[5]
	   self.adj6 = gtk.Adjustment(current_sec, 0.0, 59.0, 1.0, 5.0, 0.0)
           self.spinner6 = gtk.SpinButton(self.adj6, 0, 0)
           self.spinner6.set_wrap(True)
           vbox2.pack_start(self.spinner6, False, True, 0)
	   
	   vbox.pack_start(hbox2, True, False, 10)
	   
	   separator = gtk.HSeparator()
	   vbox.pack_start(separator, True, False, 10)
	   
	   hbox3 = gtk.HBox(False, 0)
           vbox.pack_start(hbox3, True, False, 0)
           button = gtk.Button("Set")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.set_click, self.window)
           hbox3.pack_start( button, True, False, 0)
           button = gtk.Button("Done")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.destroy_main, self.window)
           #button.set_flags(gtk.CAN_DEFAULT)
           hbox3.pack_start( button, True, False, 0)
	   
	   self.window.add(vbox)
           self.window.show_all()