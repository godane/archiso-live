# rootpw.py - set root password for installed system
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
from rootpw_gui import PWEnter
from dialogs import popupMessage

class Widget(Stage):
    def getHelp(self):
        return _("You should enter a hard-to-guess password for the root"
                " account on the newly installed system. Use a mixture of"
                " letters, digits and other characters. The password may"
                " be left empty, but that will make it more difficult to"
                " make use of the root account for system administration.\n\n"
                "If you are not a linux expert, you are strongly advised"
                " not to lose/forget the password you set here.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        self.pwe = self.addWidget(PWEnter())
        self.reinit()

    def reinit(self):
        self.request_soon(self.pwe.move_focus)

    def forward(self):
        # Check entered passwords are identical
        pw = self.pwe.get_text1()
        if (pw != self.pwe.get_text2()):
            popupMessage(_("The passwords are not identical,\n"
                    "  Please try again."))

        # Set the password
        elif install.set_rootpw(pw):
            return 0

        self.reinit()
        return -1

#################################################################

moduleName = 'RootPass'
moduleDescription = _("Set Administrator Password")
