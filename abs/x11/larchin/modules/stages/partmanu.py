# partmanu.py - manual partitioning stage
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

class Widget(Stage):
    def getHelp(self):
        return _("Here you can choose a partitioning tool and/or disk(-like)"
                " device in order to prepare your system to receive an"
                " Arch Linux installation.\n\n"
                "'cfdisk' is a console based tool which should always be"
                " available. It must be started with the name of the"
                " device on which it is to be used.\n\n"
                "'gparted' is a fancy gui-tool which can do much more,"
                " including resizing partitions, but it  may not always"
                " be available. The device to be edited can be selected"
                " from within the program.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        ld = install.listDevices()

        # Offer gparted - if available
        if (install.gparted_available() == ""):
            gparted = self.addOption('gparted',
                    _("Use gparted (recommended)"), True)
        else:
            gparted = None

        # Offer cfdisk on each available disk device
        mounts = install.getmounts().splitlines()
        mounteds = 0
        i = 0
        if ld:
            for d, s, n in ld:
                i += 1
                # Determine devices which have mounted partitions
                dstring = "%16s  (%10s : %s)" % (d, s, n)
                style = None
                for m in mounts:
                    if m.startswith(d):
                        style = 'red'
                        mounteds += 1
                        break
                self.addOption('cfdisk-%s' % d,
                        _("Use cfdisk on %s (%s)") % (d, s),
                        (i == 1) and not gparted,
                        style=style)

        else:
            popupError(_("No disk(-like) devices were found,"
                    " so Arch Linux can not be installed on this machine"))
            mainWindow.exit()

        if mounteds:
            self.addLabel(_('WARNING: Editing partitions on a device with'
                    ' mounted partitions (those marked in red) is likely'
                    ' to cause a lot of trouble!\n'
                    'If possible, unmount them and then restart this'
                    ' program.'), style='red')

        # Offer 'use existing partitions/finished'
        self.done = self.addOption('done',
                _("Use existing partitions / finished editing partitions"))


    def forward(self):
        sel = self.getSelectedOption()
        if (sel == 'gparted'):
            install.gparted()
            return -1

        elif (sel == 'done'):
            return 0

        else:
            install.cfdisk(sel.split('-')[1])
            return -1


#################################################################

moduleName = 'ManuPart'
moduleDescription = _("Edit Partitions Manually")
