# end.py - last - 'completed' - stage
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
        return _("For any further help please contact the authors.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)
        self.addLabel(_("If all went well, your installation should now"
                " be bootable. Click on OK to quit the installer."))

    def forward(self):
        return 0

#################################################################

moduleName = 'End'
moduleDescription = _("Finished!")
