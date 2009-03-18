# welcome.py - first - 'welcome' - stage
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

class Widget(Stage):
    def __init__(self):
        Stage.__init__(self, moduleDescription)
        self.addLabel(_('This will install Arch Linux'
                ' from this "live" system on your computer.'
                ' This program was written'
                ' for the <i>larch</i> project:\n'
                '       http://larch.berlios.de\n'
                '\nIt is free software,'
                ' released under the GNU General Public License.\n\n') +
                'Copyright (c) 2008   Michael Towers')

    def getHelp(self):
        return _("This installation program concentrates on just the most"
                " essential aspects of Arch Linux system installation: disk"
                " preparation, copying of the system data, generation of"
                " the initramfs, setting up the GRUB bootloader and setting"
                " the root password.\n"
                "The remaining configuration of the system can be performed"
                " before running this program. This is one advantage of"
                " installing from a 'live' system - the configuration can"
                " be set up and tested before installation.\n"
                "Configuration can of course also be performed later, on"
                " the running installed system, if you prefer.\n\n"
                "Simple graphical programs for setting the xorg keyboard"
                " layout (xkmap), for adding users (luser) and for setting"
                " the locale (localed) are available in the larch repository,"
                " and may be found in the 'system' category of the menu if"
                " they have been installed.\n\n"
                "Other useful sources of information concerning"
                " installation are the Arch Linux Installation Guide, and"
                " the Arch Linux wiki, for example the Beginner's Guide.\n\n"
                "Click on the 'OK' button to start.")

    def forward(self):
        return 0


#################################################################

moduleName = 'Welcome'
moduleDescription = _('Welcome to <i>larchin</i>')

