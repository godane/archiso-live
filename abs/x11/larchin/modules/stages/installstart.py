# installstart.py - summarize formatting and installation partitions
#
# (c) Copyright 2008, 2009 Michael Towers <gradgrind[at]online[dot]de>
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
# 2009.02.18

from stage import Stage
from installstart_gui import PartTable

import re

class Widget(Stage):
    def getHelp(self):
        return _("If you press OK now the chosen partitions will be"
                " formatted and mounted and then the running system will"
                " be copied onto them.\n"
                "You can choose to use UUID rather than device names"
                " (/dev/sda1 etc.) in /etc/fstab and GRUB. Although the"
                " UUIDs look long, ugly and unmanageable, this has"
                " the advantage that if - as can happen in systems with"
                " more than one disk - the device names get swapped your"
                " system will still work.\n"
                "The UUID choice is made separately for swap because on"
                " computers where a swap partition is shared between"
                " different linux installations, it can happen that"
                " a new installation changes the UUID (mean, but possible)."
                " Then you must weigh up which danger is most likely."
                " larchin should not change the UUID of an existing swap"
                " partition.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        self.addLabel(_("Please check that the formatting of the"
                " following partitions and their use within the new"
                " installation (mount-points) corresponds with what you"
                " had in mind. Accidents could well result in serious"
                " data loss."))

        # List of partitions configured for use.
        #    Each entry has the form [mount-point, device, format,
        #                         format-flags, mount-flags]
        parts = install.get_config("partitions", False)
        plist = []
        if parts:
            for p in parts.splitlines():
                pl = p.split(':')
                plist.append(pl + [self.getsize(pl[1])])

        # In case of mounts within mounts
        plist.sort()

        # Swaps ([device, format, include])
        swaps = install.get_config("swaps", False)
        if swaps:
            for s in swaps.splitlines():
                p, f, i = s.split(':')
                if i:
                    plist.append(["swap", p, f, "", "", self.getsize(p)])

        self.addWidget(PartTable(plist))

        self.uuid = self.addCheckButton(_("Use UUID instead of device name"))
        self.setCheck(self.uuid, install.use_uuid)
        self.uuid_swap = self.addCheckButton(
                _("Use UUID instead of device name for swaps"))
        self.setCheck(self.uuid_swap, install.use_uuid_swap)

    def getsize(self, part):
        """Get the size of a partition using the output of 'get-partsize'.
        """
        s = install.get_partsize(part)
        if s:
            return s.strip()
        else:
            return "???"

    def forward(self):
        install.use_uuid = self.getCheck(self.uuid)
        install.use_uuid_swap = self.getCheck(self.uuid_swap)
        return 0


#################################################################

moduleName = 'InstallStart'
moduleDescription = _("Confirmation")

