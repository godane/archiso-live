# swaps.py - formatting swap partitions (expert mode only)
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
    def getHelp(self):
        return _("Any existing swap partitions on the drives will be found"
                 "  and offered for formatting. It is generally good to have"
                 " a swap partition, but it is not necessary if you have more"
                 " memory than you will ever need.\n\n"
                 " 0.5 - 1.0 GB of swap space should be plenty for most"
                 " purposes.")

    def __init__(self):
        """
        """
        Stage.__init__(self, moduleDescription)

        self.swaps = {}
        inuse = install.getActiveSwaps()
        self.done = []
        if inuse:
            self.addLabel(_("The following swap partitions are currently"
                    " in use and will not be formatted (they shouldn't"
                    " need it!)."))
        for p, s in inuse:
            b = self.addCheckButton("%12s - %s %4.1f GB" % (p, _("size"), s))
            self.setCheck(b, True)
            self.done.append(p)
            self.swaps[p] = b

        all = install.getAllSwaps()
        fmt = []
        for p, s in all:
            if not (p in self.done):
                fmt.append((p, s))
        if fmt:
            self.addLabel(_("The following swap partitions will be formatted"
                    " if you select them for inclusion."))
        for p, s in fmt:
            b = self.addCheckButton("%12s - %s %4.1f GB" % (p, _("size"), s))
            self.setCheck(b, True)
            self.swaps[p] = b

        if not all:
            self.addLabel(_("There are no swap partitions available. If the"
                    " installation computer does not have a large amount of"
                    " memory, you are strongly advised to create one before"
                    " continuing."))

    def forward(self):
        config = ""
        for p, b in self.swaps.items():
            f = "" if self.done else "format"
            i = "include"if self.getCheck(b) else ""
            if config:
                config += "\n"
            config += "%s:%s:%s" % (p, f, i)
        install.set_config("swaps", config)

        return 0


#################################################################

moduleName = 'Swaps'
moduleDescription = _("Include Swap Partitions")
