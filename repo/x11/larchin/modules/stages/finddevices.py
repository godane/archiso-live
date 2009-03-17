# finddevices.py - discover possible (disk-like) installation devices
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

from stage import Stage
from dialogs import popupError, popupMessage

class Widget(Stage):
    def getHelp(self):
        return _('On the basis of the detected disk(-like) devices a choice'
                ' of devices for automatic partitioning will be offered.\n'
                'Only devices with no mounted partitions will be offered'
                ' for automatic partitioning, any others will be listed but'
                ' will not be selectable.\n'
                'The automatically calculated partitioning scheme'
                ' allows only a limited amount of tweaking, so if you want'
                ' more control over the partitioning of your disk'
                ' drives and the location of the installation, you will'
                ' need to select manual partitioning. This will normally'
                ' allow the use of the external tools cfdisk and gparted.\n'
                'In the case of manual partitioning the selection of the'
                ' mount points is done separately in the'
                ' "Select Installation Partitions" stage, which will be'
                ' skipped if the automatic partitioning scheme is accepted.\n'
                'Selecting one of the devices offered for automatic'
                ' partitioning will not immediately cause it to be modified,'
                ' so try it out without fear. You can return here via the'
                ' stage menu.')

    def __init__(self):
        Stage.__init__(self, moduleDescription)
        self.addLabel(_('Disk(-like) devices will be detected and offered'
                ' for automatic partitioning.\n\n'
                'If a device has mounted partitions it will not be offered'
                ' for automatic partitioning. If you want to partition'
                ' such a device, you must select the "Manual Partitioning"'
                ' stage.'))
        self.getDevices()

    def forward(self):
        # Set device selection for automatic partitioning.
        # The value is the name of the drive ('/dev/sda', etc.).
        # An empty string is used in the case of manual partitioning.
        sel = self.getSelectedOption()
        if (sel == 'manual'):
            install.set_config('autodevice', '')
            return 1
        else:
            install.set_config('autodevice', sel)
            return 0

    def getDevices(self):
        ld = install.listDevices()
        # Note that if one of these has mounted partitions it will not be
        # available for automatic partitioning, and should thus not be
        # included in the list used for automatic installation
        mounts = install.getmounts().splitlines()
        i = 0
        if ld:
            for d, s, n in ld:
                i += 1
                # Determine devices which have mounted partitions
                dstring = "%16s  (%10s : %s)" % (d, s, n)
                dm = False
                for m in mounts:
                    if m.startswith(d):
                        dm = True
                        i -= 1
                        break
                if dm:
                    self.addLabel('***' + dstring, align='left')
                else:
                    self.addOption(d, dstring, (i == 1))
            self.addOption('manual', _("Manual partitioning"), (i == 0))

        else:
            popupError(_("No disk(-like) devices were found,"
                    " so Arch Linux can not be installed on this machine"))
            mainWindow.exit()


#################################################################

moduleName = 'FindDevices'
moduleDescription = _("Disk Discovery")
