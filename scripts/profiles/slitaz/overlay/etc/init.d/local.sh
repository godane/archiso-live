#!/bin/sh
# /etc/init.d/local.sh - Local startup commands.
#
# All commands here will be executed at boot time.
#
. /etc/init.d/rc.functions

echo "Starting local startup commands... "

if [ $(cat /proc/cmdline | grep " vesa") ]; then
	if [ -f /etc/X11/xorg.conf.vesa ]; then
		if [ -f /etc/X11/xorg.conf ]; then
			mv -f /etc/X11/xorg.conf /etc/X11/xorg.conf.old
		fi
		cp -f /etc/X11/xorg.conf.vesa /etc/X11/xorg.conf
		tazx config-xorg
	fi
fi
