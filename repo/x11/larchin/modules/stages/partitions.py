# partitions.py - Automatic partitioning and mount-point selection
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
# 2008.06.05

from stage import Stage, ShowInfoWidget
from partitions_gui import PartitionWidget
from dialogs import popupMessage, popupWarning

MINSPLITSIZE = 20.0    # GB, if less available, no /home
SWAPPZ0 = 5            # % of total, initial swap size, but:
SWAPMAX  = 2.0         # GB, max swap size
SWAPMAXPZ = 10         # % of total, max swap size, but:
SWAPDEF = 1.0          # GB, initial swap size


class Widget(Stage):
    def getHelp(self):
        return _("To make straightforward installations easier it is"
                " possible to choose a simple automatic division of your"
                " disk drive for the Arch Linux installation.\n\n"
                "WARNING: If you have an operating system already installed"
                " on this drive which you wish to keep, you must perform"
                " partitioning manually (or use the existing partitions) by"
                " selecting 'Edit disk partitions manually' (or"
                " 'Select Installation Partitions') from the stage menu.\n"
                "EXCEPTION: if the existing operating system uses the NTFS"
                " file-system (Windows), it is also possible to use automatic"
                " partitioning, if enough space is free, or has been freed"
                " by deleting or shrinking one or more NTFS partitions.\n\n"
                "Here only space after the last NTFS partition will be"
                " available for the new Linux installation. If you want to"
                " use some or all of the space occupied by Windows, you"
                " must shrink or remove the last NTS partitions first"
                " (by returning to the appropriate stage).")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        # Info on drive
        self.device = install.get_config('autodevice', trap=False)
        if not self.device:
            self.device = install.listDevices()[0][0]
        self.dinfo = install.getDeviceInfo(self.device)

        # Info: total drive size
        totalsize = self.addWidget(ShowInfoWidget(
                _("Total capacity of drive %s:  ") % self.device))
        totalsize.set(self.dinfo[0])

        # Get partition info (consider only space after NTFS partitions)
        parts = install.getParts(self.device)
        self.startpart = 1
        self.startsector = 0
        for p in parts:
            if (p[1] == 'ntfs'):
                self.startpart = p[0] + 1
                self.startsector = p[4] + 1

        avsec = (self.dinfo[1] * self.dinfo[2] - self.startsector)
        self.avG = avsec * self.dinfo[3] / 1.0e9
        if (self.startpart > 1):
            popupMessage(_("One or more NTFS (Windows) partitions were"
                    " found. These will be retained. The available space"
                    " is thus reduced to %3.1f GB.\n"
                    "Allocation will begin at partition %d.") %
                        (self.avG, self.startpart))

        self.homesizeG = 0.0
        self.swapsizeG = 0.0
        self.root = None    # To suppress writing before widget is created

        # swap size
        self.swapWidget()

        # home size
        self.homeWidget()

        # root size
        self.root = self.addWidget(ShowInfoWidget(
                _("Space for Linux system:  ")))
        self.adjustroot()

    def swapsize_cb(self, sizeG):
        self.swapsizeG = sizeG
        self.adjustroot()

    def homesize_cb(self, sizeG):
        self.homesizeG = sizeG
        self.adjustroot()

    def adjustroot(self):
        self.rootsizeG = self.avG - self.swapsizeG - self.homesizeG
        if self.root:
            self.root.set("%8.1f GB" % self.rootsizeG)

    def homeWidget(self):
        if (self.avG >= MINSPLITSIZE):
            self.home = self.addWidget(PartitionWidget(
                _("Set size of '/home' partition (GB)"),
                _("Create partition for user data (/home)"),
                _("The creation of a separate partition"
                  " for user data (in the folder /home) allows you to keep"
                  " this separate from the system files.\n"
                  "One advantage is that the operating system can later be"
                  " freshly installed without destroying your data."),
                self.homesize_cb))

            home_upper = self.avG - SWAPMAX - 5.0
            home_value = home_upper - 2.0
            self.home.set_adjust(upper=home_upper, value=home_value)
            self.home.set_on(True)

        else:
            self.addLabel(_("There is too little free space on this"
                    " drive to make a separate partition for user data"
                    " (/home) worthwhile."))

    def swapWidget(self):
        self.swap = self.addWidget(PartitionWidget(
                _("Set size of swap partition (GB)"),
                _("Create swap partition"),
                 _("No swap partition allocated.\n"
                "Unless you have more memory than you will ever need"
                " it is a good idea to set aside some disk space"
                " for a swap partition. 0.5 - 1.0 GB should be plenty"
                " for most purposes."),
                self.swapsize_cb))

        swap_upper = self.avG * SWAPMAXPZ / 100
        if (swap_upper > SWAPMAX):
            swap_upper = SWAPMAX
        swap_value = self.avG * SWAPPZ0 / 100
        if (swap_value > SWAPDEF):
            swap_value = SWAPDEF
        self.swap.set_adjust(upper=swap_upper, value=swap_value)
        self.swap.set_on(True)

    def forward(self):
        if not popupWarning(_("You are about to perform a destructive"
                " operation on the data on your disk drive (%s):\n"
                "    Repartitioning (removing old and creating new"
                " partitions)\n\n"
                "This is a risky business, so don't proceed if"
                " you have not backed up your important data.\n\n"
                "Continue?") % self.device):
            return -1

        # I'll make the sequence: root, then swap then home.
        # But swap and/or home may be absent.
        # Start partitioning from partition with index self.startpart,
        # default value (no NTFS partitions) = 1.
        # The first sector to use is self.startsector
        # default value (no NTFS partitions) = 0.

        # The actual partitioning should be done, but the formatting can
        # be handled - given the appropriate information - by the
        # installation stage.

        # Remove all existing partitions from self.startpart
        install.rmparts(self.device, self.startpart)

        secspercyl = self.dinfo[2]
        startcyl = (self.startsector + secspercyl - 1) / secspercyl
        endcyl = self.dinfo[1]
        # Note that the ending cylinder referred to in the commands
        # will not be included in the partition, it is available to
        # be the start of the next one.

        # Get partition sizes in cylinder units
        ncyls = endcyl - startcyl
        cylsizeB = secspercyl * self.dinfo[3]
        swapC = int(self.swapsizeG * 1e9 / cylsizeB + 0.5)
        homeC = int(self.homesizeG * 1e9 / cylsizeB + 0.5)
        rootC = ncyls - swapC - homeC

        startcyl = self.newpart(startcyl, endcyl, rootC,
                (swapC == 0) and (homeC == 0))
        # See partition formatting and fstab setting up for the
        # meaning of the flags
        config = "/:%s%d:ext3:%s:%s" % (self.device, self.startpart,
                install.FORMATFLAGS, install.MOUNTFLAGS)
        self.startpart += 1
        if (swapC > 0):
            startcyl = self.newpart(startcyl, endcyl, swapC,
                    (homeC == 0), True)
            install.set_config("swaps", "%s%d:format:include" %
                    (self.device, self.startpart))
            self.startpart += 1

        if (homeC > 0):
            startcyl = self.newpart(startcyl, endcyl, homeC, True)
            config += "\n/home:%s%d:ext3:%s:%s" % (self.device, self.startpart,
                    install.FORMATFLAGS, install.MOUNTFLAGS)

        install.set_config("partitions", config)
        return 0

    def newpart(self, startcyl, endcyl, size, last, swap=False):
        """Add a new partition, taking primary/extended/logical into
        account.
        """
        # Use install.makepart, passing the cylinder boundaries
        part = -1
        if (self.startpart == 4) and not last:
            self.startpart = 5
            install.makepart(self.device, 0, startcyl, endcyl)
        elif (self.startpart <= 4):
            part = self.startpart

        newstartcyl = startcyl + size
        install.makepart(self.device, part,
                startcyl, newstartcyl,
                swap)

        return newstartcyl


#################################################################

moduleName = 'AutoPart'
moduleDescription = _("Automatic Partitioning")

