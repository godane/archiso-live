# installstart.py - summarize formatting and installation partitions
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

from stage import Stage, Report
from doinstall_gui import Progress

class Widget(Stage):
    def getHelp(self):
        return _("The installation process is now running. The individual"
                " operations being performed are listed in the report"
                " window.\n\n"
                "1) Format swap partitions.\n"
                "2) Format installation partitions.\n"
                "3) Mount installation partitions.\n"
                "4) Copy system to installation partitions.\n"
                "5) Generate new initramfs.\n"
                "6) Generate new /etc/fstab.\n"
                "7) Unmount installation partitions.")

    def __init__(self):
        Stage.__init__(self, moduleDescription)

        self.output = self.addWidget(Report())

        self.progress = self.addWidget(Progress(), False)

        self.request_soon(self.run)

    def run(self):
        mainWindow.sigprocess(None, self.doInstall)
        return self.stop_callback()

    def doInstall(self, arg):
        self.ok = False
        self.swaplist = []
        self.partlist = []
        if self.format():
            # Generate list of mounts for config file
            mounts = ""
            for pmf in self.partlist:
                if mounts:
                    mounts += "\n"
                mounts += "%s:%s:%s" % pmf
            install.set_config("mounts", mounts)

            # Regenerate the swaps config file
            swaps = ""
            for s in self.swaplist:
                if swaps:
                    swaps += "\n"
                swaps += "%s::include" % s
            install.set_config("swaps", swaps)

            if install.mount():
                for p, m, f in self.partlist:
                    self.output.report(_("Mounted partition %s at %s")
                            % (p, m))

                if (self.install() and install.unmount()):
                    self.output.report(_("Unmounted installation"
                            " partitions."))
                    self.output.report(_("\nInstallation completed"
                            " successfully."))
                    self.output.report(_("\nPress 'OK' to continue"))
                    self.ok = True
                else:
                    self.output.report(_("\nInstallation failed"))
            else:
                self.output.report(_("Couldn't mount installation"
                        " partition(s)"))

    def format(self):

        #print "NOT FORMATTING"
        #return True

        # Swaps ([device, format, include])
        for p, f, i in install.getswaps():
            if f:
                self.output.report(_("Formatting partition %s as swap ...")
                        % p)
                result = install.swapFormat(p)
                if result:
                    self.output.report(result)
                    return False
            if i:
                self.swaplist.append(p)


        # Installation partitions
        # List of partitions configured for use.
        #    Each entry has the form [mount-point, device, format,
        #                         format-flags, mount-flags]
        parts = install.get_config("partitions", False).splitlines()
        plist = [p.split(':') for p in parts]

        root = False
        if plist:
            # In case of mounts within mounts
            plist.sort()
            for mp, p, f, ff, mf in plist:
                if f:
                    self.output.report(_("Formatting partition %s as %s ...")
                            % (p, f))
                    result = install.partFormat(p, f, ff)
                    if result:
                        self.output.report(result)
                        return False
                if mp:
                    if (mp == '/'):
                        root = True
                    self.partlist.append((p, mp, mf))

        if root:
            return True
        self.output.report(_("ERROR: No root (/) partition selected"))
        return False

    def install(self):

        #print "NOT INSTALLING"
        #return True

        self.progress_count = 0
        self.progress_ratio = 1.0
        totalsize = 0
        self.output.report(_("Estimating installation size ..."))
        self.basesize = install.get_size()
        dlist = ["/bin", "/boot", "/etc", "/root", "/sbin", "/srv", "/lib",
                "/opt", "/home"]
        dlist += ["/usr/" + d for d in install.lsdir("/usr")]
        dlist.append("/var")

        self.system_size = 0
        partsizes = {}
        for d in dlist:
            gs = install.guess_size(d)
            partsizes[d] = gs
            self.system_size += gs

        self.output.report(_("Starting actual installation ...") + "\n---")
        self.progress.start()
        isize = self.basesize
        for d in dlist:
            #self.output.backline()
            self.output.report(_("--- Copying %s") % d)
            #print "cp", d, self.progress_ratio, totalsize, isize-self.basesize
            install.copyover(d, self.progress_cb)
            totalsize += partsizes[d]
            isize = install.get_size()
            self.progress_ratio = float(totalsize) / (isize - self.basesize)

        self.output.report(_("---"))
        self.output.report(_("Replacing/removing 'live'-specific stuff"))
        install.install_tidy()

        self.progress.ended()
        self.output.report(_("Copying of system completed."))
        self.output.report(_("Generating initramfs (this could take a while ...)"))
        install.mkinitcpio()
        self.output.report(_("Generating /etc/fstab"))
        install.fstab()
        return True

    def progress_cb(self):
        self.progress_count += 1
        if self.progress_count < 10:
            return
        self.progress_count = 0
        installed_size = install.get_size(log=False)
        frac = ((installed_size  - self.basesize) * self.progress_ratio
                / self.system_size)
        if (frac > 1.0):
            frac = 1.0
        self.progress.set(installed_size - self.basesize, frac)

    def forward(self):
        if self.ok:
            return 0
        else:
            return -1


#################################################################

moduleName = 'Install'
moduleDescription = _("Installing ...")

