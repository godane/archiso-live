# selpart.py - select partitions manually
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
from selpart_gui import PartitionGui, SelTable, SelDevice

import re

class Widget(Stage):
    def getHelp(self):
        return _("The device partitions used for the Arch Linux installation"
                " can be manually selected here.\n"
                "There must be at least an adequately large root ('/')"
                " partition, but the system can be split over a number of"
                " partitions, for example it is often desirable to have a"
                " separate '/home' partition to keep user data separate"
                " from system data and programs. This can be"
                " helpful when updating or changing the operating system.\n\n"
                "Also fairly common are separate partitions for one or more"
                " of '/boot', '/opt', '/usr', '/var', but it is advisable to"
                " inform yourself of the pros and cons before"
                " considering these.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        self.device = None
        self.mounts = install.getmounts()
        # List of partitions already configured for use.
        #    Each entry has the form [mount-point, device, format,
        #                         format-flags, mount-flags]
        global used_partitions
        used_partitions = []
        parts = install.get_config("partitions", False)
        if parts:
            for p in parts.splitlines():
                used_partitions.append(p.split(':'))

        self.table = SelTable()
        self.devselect = SelDevice([d[0] for d in install.listDevices()],
                self.setDevice)
        self.addWidget(self.devselect, False)

        self.addWidget(self.table)

    def setDevice(self, dev):
        if self.device:
            self.tidy()
        self.device = dev
        dinfo = install.getDeviceInfo(self.device)
        pinfo = install.getParts(self.device)
        self.table.clear()
        for p in install.getlinuxparts(self.device):
            if not self.ismounted(p):

                partno = int(re.sub("/dev/[a-z]+", "", p))
                for pi in pinfo:
                    size = 0
                    fstype = "?"
                    if (pi[0] == partno):
                        size = pi[2] * dinfo[3] # bytes
                        fstype = pi[1]
                        break

                mountp = ""
                format = ""
                fflags = ""
                mflags = ""

                # If data for partition already set up, get hold of it
                pdata = None
                for pc in used_partitions:
                    if (pc[1] == p):
                        pdata = pc
                        mountp = pc[0]
                        format = pc[2]
                        fflags = pc[3]
                        mflags = pc[4]
                        break
                if not pdata:
                    pdata = [mountp, p, format, fflags, mflags]
                    used_partitions.append(pdata)

                partobj = Partition(p, size, fstype, pdata)
                self.table.addrow(partobj)
                partobj.set_newformat(format)
                partobj.set_format_flags(fflags)
                partobj.set_mountpoint(mountp)
                partobj.set_mount_flags(mflags)

        self.table.showtable()

    def ismounted(self, part):
        return re.search(r'^%s ' % part, self.mounts, re.M)

    def tidy(self):
        """Update the information on the partitions in use as stored in
        the config file "partitions".
        """
        config = ""
        for p in used_partitions:
            if (not p[0]) and (not p[2]):
                # if no mount-point and no format, this is not interesting
                continue
            if config:
                config += "\n"
            config += "%s:%s:%s:%s:%s" % tuple(p)
        install.set_config("partitions", config)

    def forward(self):
        self.tidy()
        for p in used_partitions:
            if (p[0] == '/'):
                return 0

        popupError(_("You must specify a root ('/') partition"))
        return -1


class Partition(PartitionGui):
    """The instances of this class manage the formatting/mount
    information for a single partition.
    """
    def __init__(self, p, size, fstype, pdata):
        self.partition = p
        self.size = size        # bytes
        self.existing_format = fstype
        # The partition data is a list:
        #  [mount-point, device, format, format options, mount options]
        self.partitiondata = pdata

        PartitionGui.__init__(self)

    def has_fs(self):
        """Has the partition a file-system (either an existing one or
        one through planned formatting)? The new file-system takes precedence.
        """
        return self.partitiondata[2] or self.existing_format

    def set_mount_flags(self, mflags):
        self.partitiondata[4] = mflags
        self.set_mflags(mflags)

    def set_format_flags(self, fflags):
        self.partitiondata[3] = fflags
        self.set_fflags(fflags)

    def set_format(self, format):

        print "set_format", self.partition, format

        self.partitiondata[2] = format

        if format:
            self.reset_format_flags()
            self.reset_mount_flags()
        else:
            self.set_format_flags("")
            if not self.existing_format:
                self.set_mountpoint("")

    def set_mountpoint(self, mp, setgui=True):
        mp = mp.strip()
        if setgui:
            self.set_mp(mp)

        else:
            self.partitiondata[0] = mp
            self.reset_mount_flags()

    def reset_mount_flags(self):
        self.set_mount_flags(self.default_flags(self.mount_flags()))

    def reset_format_flags(self):
        self.set_format_flags(self.default_flags(self.format_flags()))

    def get_mount_options(self):
        mopts = []
        if self.partitiondata[0]:
            # Options only available if mount-point is set and partition
            # has (or will have) a file-system
            fl = self.mount_flags()
            if fl:
                lowermo = self.partitiondata[4].lower()
                for name, flag, on, desc in fl:
                    if flag in lowermo:
                        on = flag.upper() in self.partitiondata[4]
                    mopts.append((name, flag, on, desc))
        return mopts

    def get_format_options(self):
        fopts = []
        if self.partitiondata[2]:
            # Options only available if the partition is to be formatted
            fl = self.format_flags()
            if fl:
                lowerfo = self.partitiondata[3].lower()
                for name, flag, on, desc in fl:
                    if flag in lowerfo:
                        on = flag.upper() in self.partitiondata[3]
                    fopts.append((name, flag, on, desc))
        return fopts

    def format_flags(self):
        """Return a list of available format flags for the given
        file-system type.
        """
        # At the moment there is only an entry for 'ext3'
        return { 'ext3' : [
                (_("disable boot-time checks"), 'c', False,
                    _("Normally an ext3 file-system will be checked every"
                      " 30 mounts or so. With a large partition this can"
                      " take quite a while, and some people like to disable"
                      " this and just rely on the journalling.")),

                (_("directory indexing"), 'i', True,
                    _("This is supposed to speed up access.")),

                (_("full journal"), 'f', False,
                    _("This is supposed to increase data safety, at some"
                      " small cost in speed (and disk space?)"))
                ],
            }.get(self.partitiondata[2])

    def mount_flags(self):
        """Return a list of available mount (/etc/fstab) flags for the
        given file-system type.
        """
        # At the moment there are just these three flags
        if self.partitiondata[0]:
            flg = [ (_("noatime"), 'a', True,
                    _("Disables recording atime (access time) to disk, thus"
                      " speeding up disk access. This is unlikely to cause"
                      " problems (famous last words ...). Important for"
                      " flash devices")),

                    (_("nodiratime"), 'd', True,
                    _("Disables recording directory access time to disk, thus"
                      " speeding up disk access. This is unlikely to cause"
                      " problems (famous last words ...). Important for"
                      " flash devices")),

                    (_("noauto"), 'm', False,
                    _("Don't mount this partition during system"
                      " initialization."))
                ]

            # And nothing file-system specific
            return flg
        else:
            return None

    def default_flags(self, flist):
        """Return the default set of flags for the given list of flags
        (output of mount_flags or format_flags).
        """
        flags = ''
        if flist:
            for f in flist:
                flags += f[1].upper() if f[2] else f[1]
        return flags

    def get_used_mountpoints(self):
        """Return a list of the mount-points used by all Partition objects.
        """
        return [p[0] for p in used_partitions if p[0]]

    def get_mountpoint(self):
        return self.partitiondata[0]


#################################################################

moduleName = 'MountPoints'
moduleDescription = _("Select Install Partitions")
