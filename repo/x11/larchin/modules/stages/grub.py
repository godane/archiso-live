# grub.py - stage for setting up the boot-loader
#
# (c) Copyright 2008 Michael Towers <gradgrind[at]online[dot]de>
#
# This file is part of the larch project.
#
#    larch is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    larch is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with larch; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#----------------------------------------------------------------------------
# 2008.06.13

from stage import Stage
from grub_gui import Mbrinstall, Oldgrub
from menu_lst_base import menu_lst_base
from dialogs import popupEditor

import re
import time

class Widget(Stage):
    def getHelp(self):
        return _("GRUB allows the booting of more than one operating"
                " system.\n"
                "Normally it will be installed to the 'master boot"
                " record' on the first disk drive, but the new Linux"
                " system can also be booted from an existing GRUB.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        # Set up grub's device map and a list of existing menu.lst files.
        assert install.set_devicemap(), "Couldn't get device map for GRUB"

        self.addOption('mbr', _("Install GRUB to MBR - make it the main"
                " bootloader"), True, callback=self.mbrtoggled)
        self.mbrinstall = Mbrinstall(self)
        self.addWidget(self.mbrinstall, False)
        # What if there is >1 drive?

        if install.menulst:
            self.addOption('old', _("Add new installation to existing GRUB"
                    " menu."), callback=self.oldtoggled)
            self.oldgrub = Oldgrub(self)
            self.addWidget(self.oldgrub, False)

        self.addOption('part', _("Install GRUB to installation partition."))

        self.ntfsboot = None
        # Seek likely candidate for Windows boot partition
        dinfo = install.fdiskall()
        nlist = install.listNTFSpartitions()
        for np in nlist:
            # First look for (first) partition marked with boot flag
            if re.search(r"^%s +\*" % np, dinfo, re.M):
                self.ntfsboot = np
                break
        if (not self.ntfsboot) and nlist:
            # Else just guess first NTFS partition
            self.ntfsboot = nlist[0]

        self.request_soon(self.init)

    def init(self):
        self.setOption('part')
        self.setOption('mbr')
        return self.stop_callback()

    # Stuff for 'include existing menu'
    def mbrtoggled(self, on):
        self.mbrinstall.set_enabled(on)

    def setimport_cb(self, devpath):
        self.menulstwhere = devpath
        self.menulst = self.revert_cb()

    def editmbr_cb(self):
        newtext = popupEditor(_("Edit menu.lst"), self.menulst, self.revert_cb)
        if newtext:
            self.menulst = newtext

    def revert_cb(self):
        # Get template
        text = menu_lst_base

        # Add entries for new installation
        text += self.newgrubentries()

        # add old entries
        if self.menulstwhere:
            dev, path = self.menulstwhere.split(':')
            ml = install.readmenulst(dev, path)
            # Take everything from the first 'title'
            mlp = re.compile(".*?^(title.*)", re.M | re.S)
            m = mlp.search(ml)
            if m:
                text += "\n" + m.group(1)

        return text

    # Stuff for 'use existing menu'
    def oldtoggled(self, on):
        self.oldgrub.set_enabled(on)

    def setml_cb(self, devpath):
        self.mlwhere = devpath
        self.ml = self.reml_cb()

    def editml_cb(self):
        newtext = popupEditor(_("Edit existing menu.lst"), self.ml,
                self.reml_cb)
        if newtext:
            self.ml = newtext

    def reml_cb(self):
        if self.mlwhere:
            # Get existing menu.lst
            dev, path = self.mlwhere.split(':')
            text = install.readmenulst(dev, path)

            # Add entries for new installation
            text += "\n" + self.newgrubentries()
        else:
            text = None
        return text

    def newgrubentries(self):
        # look for separate boot partition
        self.bootpart = None
        for d, m, f in install.getumounts():
            if (m == '/'):
                self.rootpart = d
            elif (m == '/boot'):
                self.bootpart = d
        # add an entry for each initramfs
        text = "# ++++ Section added by larchin (%s)\n\n" % time.ctime()

        kernel, inits = install.getbootinfo()
        if self.bootpart:
            rp = install.grubdevice(self.bootpart)
            bp = ""
        else:
            rp = install.grubdevice(self.rootpart)
            bp = "/boot"
        for init in inits:
            text += "title  Arch Linux %s (initrd=/boot/%s)\n" % (
                    self.rootpart, init)
            text += "root   %s\n" % rp
            text += "kernel %s/%s root=%s ro\n" % (bp, kernel, self.rootpart)
            text += "initrd %s/%s\n\n" % (bp, init)

        if self.ntfsboot:
            text += "title Windows\n"
            text += "rootnoverify %s\n" % install.grubdevice(self.ntfsboot)
            text += "makeactive\n"
            text += "chainloader +1\n\n"

        return (text + "# ---- End of section added by larchin\n")

    def getmenu(self, filestring):
        """Try to extract grub entries from the given menu.lst file contents
        (in the form of a string). Return as a list.
        """
        titles = []
        lines = filestring.splitlines(True)
        reading = False
        for l in lines:
            ls = l.strip()
            if reading:
                if (not ls) or (ls == '#'):
                    titles.append(thisone)
                    reading = False
                else:
                    thisone += l
            elif ls.startswith('title'):
                reading = True
                thisone = l
        if reading:
            titles.append(thisone + '\n')
        return titles


    def forward(self):
        opt = self.getSelectedOption()
        if (opt == 'mbr'):
            device = self.mbrinstall.get_drive()
            path = None
            text = self.menulst
        elif (opt == 'old'):
            device = None
            path = self.mlwhere
            text = self.ml
        else:
            assert (opt == 'part'), "No option selected"
            if self.bootpart:
                device = self.bootpart
            else:
                device = self.rootpart
            path = None
            self.menulstwhere = None
            text = self.revert_cb()

        install.setup_grub(device, path, text)

        return 0


#################################################################

moduleName = 'Grub'
moduleDescription = _("Configure Bootloader")

