#!/usr/bin/env python
#
# larchin - A hard-disk installer for Arch Linux and larch
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

import os, sys

basedir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append("%s/modules" % basedir)
sys.path.append("%s/modules/gtk" % basedir)

from install import installClass
from guimain import Larchin
from dialogs import popupError

def errorTrap(type, value, tb):
    etext = "".join(traceback.format_exception(type, value, tb))
    popupError(etext, _("This error could not be handled."))
    if initialized:
        try:
            install.tidyup()
        except:
            pass
    quit()


import __builtin__
def tr(s):
    return s
__builtin__._ = tr

import traceback
initialized = False

sys.excepthook = errorTrap

transfer = False
if (len(sys.argv) == 1):
    target = None
elif (len(sys.argv) == 2):
    target = sys.argv[1]
else:
    popupError(_("Usage:\n"
        "          larchin.py \t\t\t\t # local installation\n"
        "          larchin.py target-address \t # remote installation\n"),
        _("Bad arguments"))
    quit()

def plog(text):
    """A function to log information from the program.
    """
    #print text
    mainWindow.reportw.report(text)

__builtin__.plog = plog
__builtin__.basePath = basedir
__builtin__.stages = {}
__builtin__.stageSwitch = {}
__builtin__.mainWindow = Larchin()
__builtin__.install = installClass(target)
initialized = True

import imp
mlist = []
# I might change this to import all .py files in the stages folder ...
for module in ('welcome', 'ntfs', 'finddevices', 'partitions', 'partmanu',
        'swaps', 'selpart', 'installstart', 'installrun', 'rootpw',
        'grub', 'end'):
    m = imp.load_source(module, "%s/modules/stages/%s.py" % (basedir, module))
    mlist.append((m.moduleName, m.moduleDescription))
    stages[m.moduleName] = m

mainWindow.setStageList(mlist)

# The following list determines the stage transitions.
# The first entry on a line is the present stage, the subsequent entries
# are the possible subsequent stages, which will be selected by index.
stageSwitchSource = """
Welcome:NtfsShrink
NtfsShrink:FindDevices
FindDevices:AutoPart:ManuPart
AutoPart:InstallStart
ManuPart:Swaps
Swaps:MountPoints
MountPoints:InstallStart
InstallStart:Install
Install:RootPass
RootPass:Grub
Grub:End
End:/
"""

# Build a dictionary for the stage transitions
for line in stageSwitchSource.splitlines():
    line = line.strip()
    if line and (line[0] != '#'):
        item = line.split(':')
        stageSwitch[item[0]] = item[1:]

mainWindow.selectStage('Welcome')
mainWindow.mainLoop()



# What about generated .pyc files? Should the package include pre-compiled
# versions?
