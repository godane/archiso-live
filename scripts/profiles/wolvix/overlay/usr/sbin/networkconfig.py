#!/usr/bin/env python

# Program to configure Wolvix network interfaces
#
# License:	GNU General Public license
# Author: 	Chris Gallienne
#
# Note: This script was wholly written by me, but I have based it on
# the zenwalk networkconfig bash script, which I have translated to
# python/gtk2 and modified/extended for wolvix. 
#
# zenwalk network config is copyright Jean-Philippe Guillemin <jp.guillemin@free.fr>. 
# and is free software under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version. Please take a look at http://www.gnu.org/copyleft/gpl.htm

import pygtk
pygtk.require('2.0')
import gtk, os, sys

from wirelessconfig import *

class NetConfig:
	
	def destroy_main(self, widget):
           self.window.destroy()
   
        def destroy_card(self, widget):
           self.card_window.destroy()
	
	def help_click(self, widget, data=None):

		def close_help (self):
			window.destroy()

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_size_request(480, 490)
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_resizable(False)
		window.set_title("Wolvix Network Configuration Help")
		window.set_border_width(10)

		fixed = gtk.Fixed()

		sw = gtk.ScrolledWindow()
		sw.set_shadow_type(gtk.SHADOW_IN)
		sw.set_size_request(430, 400)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textbuffer = gtk.TextBuffer()
		textbuffer.set_text("Program to configure network interfaces\n\
\n\
License:	GNU General Public license\n\
Author: 	Chris Gallienne\n\
Date:	30th June 2007\n\
\n\
WARNING: This program is in development. Use it at your own risk! \n\n\
USAGE:\n\
The Network Config window displays basic information about your \
network setup: Network Interfaces detected, with ip/netmask if \
the device is active; DNS server and Default Gateway ID; and \
your hostname.domainname.\n\n\
You can change/configure any of these items by double-clicking \
it in the list. This will bring up one of these configuration boxes:\n\n\
Network Interface Card:\n\
A configuration box allowing you to setup the way the device is used, \
whether to use dhcp, if so, the dhcp host ip and timeout value, if not, \
the device ip and netmask, etc. \n\n\
If the device is a wireless interface, you can also select wireless \
parameters such as essid, security mode & key, etc. Security  mode \
may be 'open', WEP or WPA. Note- WPA mode not working at this time.\n\n\
Selecting status and entering the value 'up' will restart the device \
with the new configuration you have entered.\n\n\
DNS Servers:\n\
Displays/Allows the user to enter up to three Domain Name Servers for the \
system.\n\n\
Default Gateway:\n\
Displays/Allows user to change the ip address of the default gateway to be \
used with this interface.\n\n\
Host & Domain name:\n\
Displays/allows the user to  change the system Hostname and domain- \
name\n\n\
Restart Network:\n\
Calls /etc/rc.d/rc.inet1 restart to restart all interfaces marked as 'up'.")
		textview.set_buffer(textbuffer)
		sw.add(textview)
		fixed.put(sw, 15, 15)

		button = gtk.Button("Close")
		button.set_size_request(80, 30)
		button.connect("clicked", close_help)
		fixed.put(button, 200, 430)
		window.add(fixed)
                window.show_all()

        def about (self):
                def close_help (self):
                    window.destroy()
            
                window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#window.set_size_request(300, 220)
                window.set_position(gtk.WIN_POS_CENTER)
		window.set_resizable(False)
		window.set_title("Wolvix Network Configuration")
		window.set_border_width(10)

		fixed = gtk.Fixed()

		sw = gtk.ScrolledWindow()
                sw.set_shadow_type(gtk.SHADOW_IN)
		sw.set_size_request(260, 140)
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		textview = gtk.TextView()
		textview.set_wrap_mode(gtk.WRAP_WORD)
		textbuffer = gtk.TextBuffer()
		textbuffer.set_text(" Program to configure network interfaces\n\
\n\
 License:	GNU General Public license\n\
 Author: 	Chris Gallienne\n\
 Date:	30th January 2007\n\
\n\
 WARNING: This program is in development. Use it at your own risk!")
		textview.set_buffer(textbuffer)
		sw.add(textview)
		fixed.put(sw, 15, 15)

		button = gtk.Button("Close")
		button.set_size_request(80, 30)
		button.connect("clicked", close_help)
		fixed.put(button, 110, 170)
		window.add(fixed)
		window.show_all()

        def write_inet1(self, widget, line_id, text):
             file = open('/etc/rc.d/rc.inet1.conf')
             rcinet1 = file.read()
             file.close()
             os.unlink("/etc/rc.d/rc.inet1.conf")
             file = open("/etc/rc.d/rc.inet1.conf", 'w')
             lines = rcinet1.split("\n", sys.maxint)
             found = False
	     #print "Looking for line: %s" %line_id
	     for line in lines:
                if (line.count(line_id)):
		   #print "Writing %s = '%s'" %(line_id, text)
		   line = line_id + '="' + text + '"';
                   found = True              
                file.write("%s\n" % line)
             file.close()
	     if found == False:
		#print "Failed to find line: %s" %line_id
	        os.unlink("/etc/rc.d/rc.inet1.conf")
                file = open("/etc/rc.d/rc.inet1.conf", 'w')
                lines = rcinet1.split("\n", sys.maxint)
                for line in lines:
		   seek = "# Config information for %s" %self.device
                   if (line.count(seek)):
                      file.write("%s\n" %seek)
		      line = line_id + '="' + text + '"';
                      found = True              
                      #print "Writing line: %s" %line
		   file.write("%s\n" % line)
                file.close()
	            
             self.make_listbox(self)
             self.make_cardlistbox(self)
             self.card_window.show_all()
             self.window.show_all()

        def dev_update(self, widget, text):
            wireless = False
	    for devices in self.device_list:
                if (devices['name']==self.device):
			device = devices
			if devices['wireless']:
				wireless = True
	    window = gtk.Dialog(text, None, gtk.DIALOG_MODAL, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            window.set_position(gtk.WIN_POS_CENTER)
            print "Setting device %s %s\n" %(devices['name'], text)
	    if text == "STATUS":
                choice = "(up/down)"
            elif text == "IPADDR" or text == "DHCP_HOSTNAME":
                choice = ""
            elif text == "DHCP_TIMEOUT":
                choice = "(e.g. 10s)"
            elif text == "WLAN_ESSID":
                choice = "essid"
            elif text == "WLAN_MODE":
                choice = "eg. Managed"
            elif text == "WLAN_CHANNEL":
                choice = "1-14 or auto"
            elif text == "WLAN_SECURITY":
                choice = "WEP, WPA or NONE"
            elif text == "WLAN_KEY":
                choice = ""
            else:
                choice = "(yes/no)"
            label = gtk.Label("Set value for %s %s:" %(self.device, choice))
            window.vbox.pack_start(label, True, False, 0)
            dns_entry1 = gtk.Entry(64)
            window.vbox.pack_start(dns_entry1, True, True, 10)
            window.show_all()
            response = window.run()
            line_id = "%s[" %text
            line_id = line_id + self.device[3:] + "]"
            if (response == gtk.RESPONSE_ACCEPT):
                if text == "STATUS":
                    self.write_inet1(self, line_id, dns_entry1.get_text())
                    if (dns_entry1.get_text())=="up":
			#os.system("ifconfig %s %s" %(self.device, dns_entry1.get_text()))
			os.system("/etc/rc.d/rc.inet1 %s_start" %self.device)
			#if (device['use_dhcp']=="yes"):
			#    os.system("dhcpcd -d -t 8 %s" %device['name'])
		    else:
			os.system("/etc/rc.d/rc.inet1 %s_stop" %self.device)
			#os.system("ifconfig %s %s" %(self.device, dns_entry1.get_text()))
		#if text == "USE_DHCP":
                 #   self.write_inet1(self, line_id, dns_entry1.get_text())
                 #   os.system("ifconfig %s %s" %(self.device, dns_entry1.get_text()))
                else:
                    self.write_inet1(self, line_id, dns_entry1.get_text())
            self.make_listbox(self)
            self.make_cardlistbox(self)
            self.card_window.show_all()
            self.window.show_all()
	    window.destroy()
            
        def settingActivated(self, treeview, path, data = None):
            selection = treeview.get_selection()
            (model, iter) = selection.get_selected()
            id = model.get_value(iter, 0)
            for devices in self.device_list:
                if (devices['name']==self.device):
			device = devices
	    if (id.count("Status")):
                self.dev_update(None, "STATUS")
            if (id.count("Use DHCP")):
                self.dev_update(None, "USE_DHCP")		    
            if (id.count("DHCP timeout")):
                self.dev_update(None, "DHCP_TIMEOUT")		    
            if (id.count("Keep DNS")):
                self.dev_update(None, "DHCP_KEEPRESOLV")		    
            if (id.count("Keep GW")):
                self.dev_update(None, "DHCP_KEEPGW")		    
            if (id.count("IP Address")):
                if device['state']=="down":
			self.dev_update(None, "IPADDR")	
		else:
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
				"Set status = 'down' before changing this value.")
			resp = message.run()
			message.destroy()
            if (id.count("Network mask")):
                if device['state']=="down":
		    self.dev_update(None, "NETMASK")		    
		else:
			message = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
				"Set status = 'down' before changing this value.")
			resp = message.run()
			message.destroy()
	    if (id.count("DHCP Host")):
                self.dev_update(None, "DHCP_HOSTNAME")		    
            
        def make_cardlistbox(self, widget):
            self.card_store.clear()
            self.card_column1.clear()
            self.card_column2.clear()
            # Get network interface status
            for devices in self.device_list:
                if (devices['name']==self.device):
                    self.card_store.append(["Status", devices['state']])
                    self.card_store.append(["Use DHCP", devices['use_dhcp']]) 
		    if (devices['use_dhcp']=='yes'):
		        self.card_store.append(["DHCP Host", devices['dhcp_hostname']]) 
                        self.card_store.append(["DHCP timeout", devices['dhcp_timeout']]) 
                    self.card_store.append(["Keep DNS", devices['dhcp_keepresolv']]) 
                    self.card_store.append(["Keep GW", devices['dhcp_keepgw']]) 
                    if (devices['use_dhcp']=='no'):
		        self.card_store.append(["IP Address", devices['ip']]) 
                        self.card_store.append(["Network mask", devices['netmask']]) 
            renderer1 = gtk.CellRendererText()
            self.card_column1.pack_start(renderer1)
            self.card_column1.set_attributes(renderer1, text = 0)
            renderer2 = gtk.CellRendererText()
            self.card_column2.pack_start(renderer2)
            self.card_column2.set_attributes(renderer2, text = 1)
            
        def netcard_config(self, widget, model, iter):
            self.device = model.get_value(iter, 0)
            self.card_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
            self.card_window.connect("destroy", self.destroy_card)
            self.card_window.set_title("%s settings" %self.device)
            self.card_window.set_border_width(0)
            vbox = gtk.VBox(False, 0)
            hbox1 = gtk.HBox(False, 0)
            image = gtk.Image()
            scrolled_window = gtk.ScrolledWindow()
            scrolled_window.set_border_width(10)
            scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            for devices in self.device_list:
                if (devices['name']==self.device):
                    label1 = gtk.Label("\nLinked:  %s\nDriver:   %s\n" 
                                                  %(devices['link'], devices['driver']))
                    scrolled_window.set_size_request(240, 200)
		    image.set_from_file("/usr/share/icons/Tango/scalable/devices/network-wired.svg")
            hbox1.pack_start(image, True, False, 15)
            vbox.pack_start(hbox1, True, False, 0)
            label1.set_line_wrap(True)
            hbox1.pack_start(label1, True, False, 15)
            vbox.pack_start(scrolled_window, True, True, 0)
            table = gtk.Table(1, 1, False)
            scrolled_window.add_with_viewport(table)
            self.card_store = gtk.ListStore(str, str)
            self.card_listControl = gtk.TreeView(self.card_store)
            self.card_column1 = gtk.TreeViewColumn("")
            self.card_column2 = gtk.TreeViewColumn("")
            self.card_listControl.append_column(self.card_column1)	   
            self.card_listControl.append_column(self.card_column2)	   
            self.make_cardlistbox(self)
            table.attach(self.card_listControl, 0, 1, 0, 1)
            hbox = gtk.HBox(False, 0)
            button = gtk.Button("Done")
            button.set_size_request(100, 30)
            button.connect_object("clicked", self.destroy_card, self.card_window)
            #button.set_flags(gtk.CAN_DEFAULT)
            hbox.pack_start( button, True, False, 0)
            vbox.pack_start( hbox, False, False, 10)
            self.card_listControl.connect('row-activated', self.settingActivated)
            self.card_window.add(vbox)
            self.card_window.show_all()
   
        def get_member(self, widget, device, dir):
          path = "/sys/class/net/" + device + dir
          os.system("cat %s > /tmp/carrier.txt" %path)
          for line in file('/tmp/carrier.txt').readlines():
              word = line.split()
              self.member = word[0]

        def get_feature(self, widget, param, device, item):
          if (device.count("ath")):
		device = device.replace("ath", "wifi")
	  os.system("ethtool %s %s > /tmp/feature.txt" %(param, device))
          for line in file('/tmp/feature.txt').readlines():
              if (line.count(item)):
                 word = line.split()
                 self.member = word[1]
	  
        def get_netinfo(self, widget):
            # getting current DNS parameters
            info = ""
            for line in file('/etc/resolv.conf').readlines():
                word = line.split()
                if (word[0] == "nameserver"):
                    if info != "":
                        info = info + " "
                    info = info + word[1] 
	    self.netinfo_list['dns_server'] =info
            # getting current Gateway
            os.system("route -n > /tmp/netinfo.txt")
            for line in file('/tmp/netinfo.txt').readlines():
                word = line.split()
                if (word[0] == "0.0.0.0"):
                    self.netinfo_list['default_gateway'] = (word[1])
	    # getting hostname & domain name
            for line in file('/etc/HOSTNAME').readlines():
                word = line.split('\n')
		word = word[0].split('.')
                self.netinfo_list['hostname'] = (word[0])
		word[2].strip('\n')
                self.netinfo_list['domainname'] = (word[1]+'.'+word[2])
            #print "Net info list = %s\n" %self.netinfo_list

        def write_resolv(self, widget, text):
             words = text.split()
             file = open('/etc/resolv.conf')
             resolv = file.read()
             file.close()
             os.unlink("/etc/resolv.conf")
             file = open("/etc/resolv.conf", 'w')
             lines = resolv.split("\n", sys.maxint)
             for line in lines:
                if (not line.count("nameserver") and len(line)>2):
                   file.write("%s\n" % line)
             for word in words:
                file.write("nameserver %s\n" %word)
             file.close()
             self.make_listbox(self)
             self.window.show_all()

        def get_DNSserver(self, widget):
            window = gtk.Dialog("DNS Servers", None, gtk.DIALOG_MODAL, 
                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
            window.set_position(gtk.WIN_POS_CENTER)
            label = gtk.Label("Enter DNS server IP addresses:")
            window.vbox.pack_start(label, True, False, 0)
            word = self.netinfo_list['dns_server'].split()
            hbox = gtk.HBox(False, 0)
            label1 = gtk.Label("DNS 1")
            hbox.pack_start(label1, False, False, 10)
            dns_entry1 = gtk.Entry(15)
            if len(word)>0:
                dns_entry1.set_text(word[0])
            hbox.pack_start(dns_entry1, True, True, 10)
            window.vbox.pack_start(hbox, True, False, 0)
            hbox = gtk.HBox(False, 0)
            label2 = gtk.Label("DNS 2")
            hbox.pack_start(label2, False, False, 10)
            dns_entry2 = gtk.Entry(15)
            if len(word)>1:
                dns_entry2.set_text(word[1])
            hbox.pack_start(dns_entry2, True, True, 10)
            window.vbox.pack_start(hbox, True, False, 0)
            hbox = gtk.HBox(False, 0)
            label3 = gtk.Label("DNS 2")
            hbox.pack_start(label3, False, False, 10)
            dns_entry3 = gtk.Entry(15)
            if len(word)>2:
                dns_entry3.set_text(word[2])
            hbox.pack_start(dns_entry3, True, True, 10)
            window.vbox.pack_start(hbox, True, False, 0)
            window.show_all()
            response = window.run()
            if (response == gtk.RESPONSE_ACCEPT):
                line = dns_entry1.get_text() + " " + dns_entry2.get_text() + " " + dns_entry3.get_text()
                self.write_resolv(self, line)
            window.destroy()
    
        def write_gateway(self, widget, text):
             words = text.split()
             file = open('/etc/rc.d/rc.inet1.conf')
             inet = file.read()
             file.close()
             os.unlink("/etc/rc.d/rc.inet1.conf")
             file = open("/etc/rc.d/rc.inet1.conf", 'w')
             lines = inet.split("\n", sys.maxint)
             for line in lines:
                if (line.count("GATEWAY=")):
                    line = 'GATEWAY="%s"\n' %text
                #print "Writing new line: %s" %line
	        file.write("%s\n" % line)
             file.close()
             os.system("route del -net default")
             os.system("route add default gw %s" %text)
             self.make_listbox(self)
             self.window.show_all()

        def get_default_gateway(self, widget):
            window = gtk.Dialog("Default Gateway", None, gtk.DIALOG_MODAL, 
                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
            window.set_position(gtk.WIN_POS_CENTER)
            label = gtk.Label("Enter Gateway address:")
            window.vbox.pack_start(label, True, False, 0)
            gw_entry1 = gtk.Entry(15)
            gw_entry1.set_text(self.netinfo_list['default_gateway'])
            window.vbox.pack_start(gw_entry1, True, False, 0)
            window.show_all()
            response = window.run()
            if (response == gtk.RESPONSE_ACCEPT):
                self.write_gateway(self, gw_entry1.get_text())
            window.destroy()
    
# resolv.conf file
#    if [ "$newvalue2" ]; then
#      nodomain="$(sed -e '/^search[ \t]*.*$/d' -e '/^domain[ \t]*.*$/d' $resolv)"
#      echo "search $newvalue2" > $resolv
#      echo "domain $newvalue2" >> $resolv
#      echo "$nodomain" >> $resolv
#    fi
    
        def write_hostname(self, widget, text):
             os.unlink("/etc/HOSTNAME")
             file = open("/etc/HOSTNAME", 'w')
             file.write("%s\n" % text)
             file.close()
             word = text.split('.')
             os.unlink("/etc/hosts")
             file = open("/etc/hosts", 'w')
             file.write("#\n\
# hosts         This file describes a number of hostname-to-address\n\
#               mappings for the TCP/IP subsystem.  It is mostly\n\
#               used at boot time, when no name servers are running.\n\
#               On small systems, this file can be used instead of a\n\
#               'named' name server.  Just add the names, addresses\n\
#               and any aliases to this file...\n\
#\n\
# By the way, Arnt Gulbrandsen <agulbra@nvg.unit.no> says that 127.0.0.1\n\
# should NEVER be named with the name of the machine.  It causes problems\n\
# for some (stupid) programs, irc and reputedly talk. :^)\n\
#\n\
\n\
# For loopbacking.\n\
127.0.0.1               localhost\n\
127.0.0.1               %s.%s.%s %s\n\
\n\
# End of hosts." %(word[0], word[1], word[2], word[0]))

	     file.write("%s\n" % text)
             file.close()
             os.system("hostname --file etc/HOSTNAME")
             self.make_listbox(self)
             self.window.show_all()

        def get_host_domain(self, widget):
            window = gtk.Dialog("Host/Domain Name", None, gtk.DIALOG_MODAL, 
                (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
            window.set_position(gtk.WIN_POS_CENTER)
            label = gtk.Label("Enter your Hostname and Domain name:")
            window.vbox.pack_start(label, True, False, 0)
            hbox = gtk.HBox(False, 0)
            label1 = gtk.Label("Hostname     ")
            hbox.pack_start(label1, False, False, 10)
            dns_entry1 = gtk.Entry(15)
            dns_entry1.set_text(self.netinfo_list['hostname'])
            hbox.pack_start(dns_entry1, True, True, 10)
            window.vbox.pack_start(hbox, True, False, 0)
            hbox = gtk.HBox(False, 0)
            label2 = gtk.Label("Domain Name")
            hbox.pack_start(label2, False, False, 10)
            dns_entry2 = gtk.Entry(15)
            dns_entry2.set_text(self.netinfo_list['domainname'])
            hbox.pack_start(dns_entry2, True, True, 10)
            window.vbox.pack_start(hbox, True, False, 0)
            window.show_all()
            response = window.run()
            if (response == gtk.RESPONSE_ACCEPT):
                self.write_hostname(self, "%s.%s" %(dns_entry1.get_text(), dns_entry2.get_text()))
            window.destroy()
    
        def rowActivated(self, treeview, path, data = None):
            selection = treeview.get_selection()
            (model, iter) = selection.get_selected()
            id = model.get_value(iter, 0)
	    print "You clicked %s\n" %id
	    if (id.count("eth") or id.count("wlan") or id.count("sit")or id.count("ath")):
                for devices in self.device_list:
                    if devices['name'] == id:
			#if devices['wireless']:
			#    wirelessconfig = WirelessConfig()
			#else:
			    self.netcard_config(None, model, iter)
            if(id.count("DNS")):
                self.get_DNSserver(None)
            if(id.count("Default")):
                self.get_default_gateway(None)
            if(id.count("Host")):
                self.get_host_domain(None)
            if(id.count("Restart")):
                os.system('touch /tmp/run')
		os.system("/usr/sbin/restart_status.py 'restarting network...' & /etc/rc.d/rc.inet1 restart")
                os.system('rm /tmp/run')
		self.make_listbox(self)
		message = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, 
                                     "Network restarted!")
                resp = message.run()
                message.destroy()
            if(id.count("About")):
                self.about()
   
        def get_devices(self, widget):
           os.system("ls /sys/class/net > /tmp/eth.txt")
           for line in file('/tmp/eth.txt').readlines():
              word = line.split()
              if (not line.count("lo") and not line.count("sit")and not line.count("wifi")):
                 device = {'name': "", 'state': "", 'link': "", 'mac': "", 'driver': "", 'duplex': "",
				'speed': "", 'ip': "", 'netmask': "", 'use_dhcp': "", 'dhcp_timeout': "",
				'dhcp_keepresolv': "", 'dhcp_keepgw': "", 'dhcp_hostname': "", 'essid': "",
				'mode': "", 'channel': "", 'security': "", 'key': "", 'rate': ""}
                 device['name'] = word[0]
                 path = "/sys/class/net/" + device['name']
		 os.system("ls %s > /tmp/dev.txt" %path)
		 wireless = False
		 for line in file('/tmp/dev.txt').readlines():
			word = line.split()
			if word.count("wireless"):
				wireless = True
		 device['wireless'] = wireless
		 os.system("ifconfig -s > /tmp/ifconfig.txt")
                 state = 0
                 self.member = ""
                 for line in file('/tmp/ifconfig.txt').readlines():
                    if (line.count(device['name'])):
                       state = 1
                 if (state==1):
                    device['state'] = "up"
                    self.get_member(None, device['name'], "/carrier") 
                 else:
                    device['state'] = "down"
                 if self.member=='1':
                    device['link'] = "yes"
                 else:
                    device['link'] = "no"
                 self.get_member(None, device['name'], "/address") 
                 device['mac'] = self.member
                 self.get_feature(None, "-i", device['name'], "driver") 
                 device['driver'] = self.member
		 if (state==1):
                    self.get_feature(None, "", device['name'], "Duplex:") 
                    device['duplex'] = self.member
                    self.get_feature(None, "", device['name'], "Speed") 
                    device['speed'] = self.member
                 else:
                    device['duplex'] = ""
                    device['speed'] = ""
                 os.system("ifconfig %s > /tmp/ifconfig.txt" %device['name'])
                 print "Device = %s\n" %device
                 if (device['link']=="yes"):
			for line in file('/tmp/ifconfig.txt').readlines():
				if (line.count("inet ")):
					#print "Found inet line\n"
					word = line.split()
					device['ip'] = word[1][5:]
					device['netmask'] = word[3][5:]
				dev_ip = ""
				dev_nm = ""
		 else:
			device['ip'] = ""
			device['netmask'] = ""
			dev_ip = "IPADDR[" + device['name'][3:] + "]"
			dev_nm = "NETMASK[" + device['name'][3:] + "]"
                 use_dhcp = "USE_DHCP[" + device['name'][3:] + "]"
                 dhcp_timeout = "DHCP_TIMEOUT[" + device['name'][3:] + "]"
                 keep_dns = "DHCP_KEEPRESOLV[" + device['name'][3:] + "]"
                 keep_gw = "DHCP_KEEPGW[" + device['name'][3:] + "]"
                 dhcp_host = "DHCP_HOSTNAME[" + device['name'][3:] + "]"
                 wlan_essid = "WLAN_ESSID[" + device['name'][3:] + "]"
		 wlan_mode = "WLAN_MODE[" + device['name'][3:] + "]"
		 wlan_channel = "WLAN_CHANNEL[" + device['name'][3:] + "]"
		 wlan_security = "WLAN_SECURITY[" + device['name'][3:] + "]"
		 wlan_key = "WLAN_KEY[" + device['name'][3:] + "]"
		 for line in file('/etc/rc.d/rc.inet1.conf').readlines():
                    word = line.split()
                    if (line.count(use_dhcp)):
                       device['use_dhcp'] = word[0][12:].strip('"')
		    elif (line.count(dhcp_timeout)):
                       device['dhcp_timeout'] = word[0][16:].strip('"')
                    elif (line.count(keep_dns)):
                       device['dhcp_keepresolv'] = word[0][19:].strip('"')
                    elif (line.count(keep_gw)):
                       device['dhcp_keepgw'] = word[0][15:].strip('"')
                    elif (line.count(dhcp_host)):
                       device['dhcp_hostname'] = word[0][18:].strip('"')
                    elif (line.count(wlan_essid)):
                       device['essid'] = word[0][14:].strip('"')
                    elif (line.count(wlan_mode)):
                       device['mode'] = word[0][13:].strip('"')
                    elif (line.count(wlan_channel)):
                       device['channel'] = word[0][16:].strip('"')
                    elif (line.count(wlan_security)):
                       device['security'] = word[0][17:].strip('"')
                    elif (line.count(wlan_key)):
                       device['key'] = word[0][12:].strip('"')
                    elif (line.count(dev_ip)):
                       if (state!=1):
			  device['ip'] = word[0][11:].strip('"')
                    elif (line.count(dev_nm)):
                       if (state!=1):
                          device['netmask'] = word[0][12:].strip('"')
                    #print "Device = %s\n" %device
		
                 self.device_list.append(device)
                 
        def make_listbox(self, widget):
           self.store.clear()
           self.column1.clear()
           self.column2.clear()
           # Get network interface device info
           self.device_list = []
           self.get_devices(None)
           for devices in self.device_list:
              if (devices['state']=="up"):
                 address = devices['ip'] + "/" + devices['netmask']
                 self.store.append([devices['name'], address])
              else:
                 self.store.append([devices['name'], "down"])
              #print "Device info: %s" %devices
	   # Get network interface device info
           self.netinfo_list = {'dns_server': "", 'default_gateway': "", 'hostname': "", 'domainname': ""}
           self.get_netinfo(None)
           #print "Network info = %s" %self.netinfo_list
	   self.store.append(["DNS Servers", self.netinfo_list['dns_server']])
	   self.store.append(["Default Gateway", self.netinfo_list['default_gateway']])	
           self.store.append(["Host & Domainname", self.netinfo_list['hostname']+'.'+self.netinfo_list['domainname']])
	   self.store.append(["Restart Network", ""])
           self.store.append(["About", ""])
           renderer1 = gtk.CellRendererText()
           self.column1.pack_start(renderer1)
           self.column1.set_attributes(renderer1, text = 0)
           renderer2 = gtk.CellRendererText()
           self.column2.pack_start(renderer2)
           self.column2.set_attributes(renderer2, text = 1)
            
        def __init__(self):
           self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
           self.window.connect("destroy", self.destroy_main)
           self.window.set_title("Wolvix Network Config")
           self.window.set_border_width(0)
           #self.window.set_size_request(360, 360)
   
           vbox = gtk.VBox(False, 0)
           hbox1 = gtk.HBox(False, 0)
           image = gtk.Image()
           image.set_from_file("/usr/share/icons/Tango/scalable/devices/network-wired.svg")
           hbox1.pack_start(image, False, False, 15)
           label1 = gtk.Label("Welcome to Wolvix Network Config.\n\
Double click on item below to configure:")
           label1.set_line_wrap(True)
           hbox1.pack_start(label1, False, False, 15)
           vbox.pack_start(hbox1, True, False, 0)
        
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
           button = gtk.Button("Help")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.help_click, self.window)
           hbox2.pack_start( button, True, False, 0)
           button = gtk.Button("Done")
           button.set_size_request(100, 30)
           button.connect_object("clicked", self.destroy_main, self.window)
           #button.set_flags(gtk.CAN_DEFAULT)
           hbox2.pack_start( button, True, False, 0)
           self.listControl.connect('row-activated', self.rowActivated)
           self.window.add(vbox)
           self.window.show_all()
   
