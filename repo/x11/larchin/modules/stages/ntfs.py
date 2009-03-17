# ntfs.py - Resizing of NTS partitions
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
from ntfs_gui import NtfsWidget, ShowInfoWidget, PartitionWidget
from dialogs import popupWarning, popupMessage

class Widget(Stage):
    def getHelp(self):
        return _("If a partition is occupied by a Windows operating system"
                " (using the NTFS file-system), you have here the option of"
                " shrinking it to create enough space for Arch Linux.\n"
                "As the automatic partitioning utility only considers space"
                " after the last NTFS partition, it may under certain"
                " circumstances be necessary to delete such a partition,"
                " which can also be done here.\n"
                "If you need more sophisticated partition management you"
                " will have to resort to the manual tools. This automatic"
                " partitioning is only suitable for situations where space"
                " for the new Linux installation is to be allocated at the"
                " end of a disk, after 0 or more NTFS partitions.\n\n"
                "As the operations offered here are potentially quite"
                "destructive please consider carefully before using them.")

    def __init__(self):
        """
        """
        Stage.__init__(self, moduleDescription)

        # Info: NTFS partitions, current partition, total drive size
        self.info = self.addWidget(PartitionWidget())

        # NTFS resizing
        self.ntfs = self.addWidget(NtfsWidget(self.size_changed_cb))

        # Info: space after last NTFS partition
        self.rest = self.addWidget(ShowInfoWidget(
                _("(Potential) free space at end of drive:  ")))

        # Get a list of NTFS partitions (all disks) and then the
        # corresponding info about the disks and partitions
        self.partlist = self.getNTFSparts()
        # Each disk (with NTFS partitions) gets an entry in self.diskinfo.
        # Each entry is a list-pair: [disk info, list of partitions' info]
        # The second item, the partition-info list can be changed if a
        # partition is shrunk or removed.
        self.diskinfo = {}
        for p in self.partlist:
            d = p.rstrip("0123456789")
            if not self.diskinfo.has_key(d):
                self.diskinfo[d] = [install.getDeviceInfo(d), None]
                self.diskChanged(d)

        # List of already 'handled' partitions
        self.donelist = []

        self.reinit()

    def reinit(self):
        # Display list of ntfs partitions
        self.info.set_plist(self.partlist)

        # If no NTFS partition to handle is found, skip this stage
        self.skip = True
        dev0 = None
        for part in self.partlist:
            self.device = part.rstrip('0123456789')
            self.partitionnum = int(part[len(self.device):])

            self.dinfo, pilist = self.diskinfo[self.device]
            # self.dinfo:
            #   ( drive size as string,
            #     drive size in cylinders,
            #     cylinder size in sectors,
            #     sector size in bytes )
            # pi:
            #   [(partition-number, partition-type,
            #     size in sectors, start in sectors, end in sectors),
            #    ... ]

            # Get information on the current partition
            for pi in pilist:
                if (pi[0] == self.partitionnum):
                    # These sizes are all in sectors
                    psize, pstart, pend = pi[2:]
                    break

            # Flag last NTFS partition on device
            self.lastpart = True
            if (self.device == dev0):
                self.lastpart = False
            else:
                # Remember info for last NTFS partition on this disk.
                # These sizes are all in sectors
                self.lpsize, self.lpstart, self.lpend = psize, pstart, pend
            dev0 = self.device

            if part in self.donelist:
                # Step through partitions
                continue
            self.donelist.append(part)
            self.pstart = pstart    # Needed for resizing

            self.info.set_part(part)
            self.info.set_disksize(self.dinfo[0])
            self.skip = False
            plog("NTFS editor: %s" % part)

            self.dsize = self.dinfo[1] * self.dinfo[2]  # sectors

            self.secsize = self.dinfo[3]
            psizeG = float(psize) * self.secsize / 1e9
            self.ntfs.set_partsize("%3.1f GB" % psizeG)
            self.ntfs.set_delete(False)
            # Set the maximum shrunk size to slightly less than the
            # current partition size
            maxsizeG = psizeG - 0.2
            plog("reduced psize = %d" % maxsizeG)
            self.ntfs.set_max(maxsizeG)

            # Get occupied space, allow 200MB extra
            ntfsmin = float(install.getNTFSmin(part)) / 1e9 + 0.2
            plog("ntfsmin = %3.1f" % ntfsmin)
            if (maxsizeG < ntfsmin):
                # Too full to shrink
                self.ntfs.toofull(True)
                self.ntfs.set_delete(self.lastpart and
                        (((self.dsize-pend) * self.secsize / 1e9)
                                < install.LINUXMIN))
                return

            self.ntfs.toofull(False)
            self.ntfs.set_min(ntfsmin)

            # Whether to shrink by default?
            # Only if it is the last NTFS partition on this disk,
            # and if a fair sharing of free space calls for shrinking,
            # and if it is possible to shrink to the required extent.
            shrinkon = self.lastpart
            # How much to shrink by default?
            # Suggest sharing excess (over the minimum) equally between
            # Linux and Windows
            sizeG = (psizeG + ntfsmin) / 2
            if self.lastpart:
                excess = (self.dsize - pstart) * self.secsize / 1e9 - ntfsmin
                if excess < install.LINUXMIN:
                    # The available space is too small, propose
                    # deleting the partition
                    self.ntfs.set_delete(True)
                    sizeG = ntfsmin
                else:
                    excess -= install.LINUXMIN
                    s = ntfsmin + (excess / 2)
                    if (s < (psizeG - 0.5)):
                        # shrink unless change is only minimal
                        sizeG = s
                    else:
                        shrinkon = False

            else:
                self.set_rest(self.dsize - self.lpend)

            self.ntfs.set_size(sizeG)
            self.ntfs.set_shrink(shrinkon)
            return
        # End of for-loop

    def set_rest(self, sectors):
        self.rest.set("%8.1f GB" % (float(sectors) * self.secsize / 1e9))

    def getNTFSparts(self):
        """Return a list of NTFS partitions. Only unmounted partitions will
        be considered.
        """
        # Get list of mounted partitions
        mounts = [m.split()[0] for m in install.getmounts().splitlines()
                if m.startswith('/dev/')]

        # Get and filter list of NTS partitions
        partlist = [p for p in install.listNTFSpartitions()
                if p not in mounts]

        # Reverse the list order so that the last partitions come first
        partlist.reverse()
        return partlist

    def size_changed_cb(self, size):
        """Called when the requested shrinkage changes, by moving the slider,
        by changing the delete flag, by changing the shrink flag.
        size < 0 => delete
        size = 0 => no shrink
        size > 0 => new shrunk size, in GB
        """
        if self.lastpart:
            if (size < 0):
                # This could be wrong, if there is free space before the
                # partition
                rest = self.dsize - self.lpstart
            elif (size == 0):
                rest = self.dsize - self.lpend
            else:
                rest = self.dsize - self.lpstart - int(
                        size * 1e9 / self.secsize)
            self.set_rest(rest)

    def forward(self):
        if self.skip:
            return 0

        # Carry out the requested operation!
        devpart="%s%d" % (self.device, self.partitionnum)
        if self.ntfs.deletestate:
            install.rmpart(self.device, self.partitionnum)
            self.partlist.remove(devpart)
            self.diskChanged(self.device)

        elif self.ntfs.shrinkstate and popupWarning(
                _("You are about to shrink %s."
                " Make sure you have backed up"
                " any important data.\n\n"
                "Continue?") % devpart):
            newsize = int(self.ntfs.size * 1e9 / self.secsize)  # sectors
            message = install.doNTFSshrink(self.device, self.partitionnum,
                    newsize, self.pstart, self.dinfo)
            if message:
                # resize failed
                popupMessage(_("Sorry, resizing failed. Here is the"
                        " error report:\n\n") + message)
            self.diskChanged(self.device)

        if (devpart == self.partlist[-1]):
            # Last NTFS partition
            return 0

        self.reinit()
        # Don't go to next stage
        return -1

    def diskChanged(self, dev):
        p = install.getParts(dev)
        self.diskinfo[dev][1] = p


#################################################################

moduleName = 'NtfsShrink'
moduleDescription = _("Modify Windows Partition")

