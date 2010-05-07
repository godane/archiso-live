#!/bin/sh
# /etc/init.d/hwconf.sh - SliTaz hardware configuration.
#
# This script configures the sound card and screen. Tazhw is used earlier
# at boot time to autoconfigure PCI and USB devices.
#
. /etc/init.d/rc.functions

# Parse cmdline args for boot options (See also rcS and bootopts.sh).
XARG=""
for opt in `cat /proc/cmdline`
do
	case $opt in
		sound=*)
			DRIVER=${opt#sound=} ;;
		xarg=*)
			XARG="$XARG ${opt#xarg=}" ;;
		screen=text)
				# Disable X.
				echo -n "Disabling X login manager: slim..."
				. /etc/rcS.conf
				RUN_DAEMONS=`echo $RUN_DAEMONS | sed s/' slim'/''/`
				sed -i s/"RUN_DAEMONS.*"/"RUN_DAEMONS=\"$RUN_DAEMONS\"/" /etc/rcS.conf
				status ;;
		screen=*)
			SCREEN=${opt#screen=} ;;
		vesa)
			export VESA="yes" ;;
		*)
			continue ;;
	esac
done

# Sound configuration stuff. First check if sound=no and remove all
# sound Kernel modules.
if [ -n "$DRIVER" ]; then
	case "$DRIVER" in
	no)
		echo -n "Removing all sound kernel modules..."
		rm -rf /lib/modules/`uname -r`/kernel/sound
		status
		echo -n "Removing all sound packages..."
		for i in $(grep -l '^DEPENDS=.*alsa-lib' /var/lib/tazpkg/installed/*/receipt) ; do
			pkg=${i#/var/lib/tazpkg/installed/}
			echo 'y' | tazpkg remove ${pkg%/*} > /dev/null
		done
		for i in alsa-lib mhwaveedit asunder libcddb ; do
			echo 'y' | tazpkg remove $i > /dev/null
		done
		status ;;
	noconf)
		echo "Sound configuration was disabled from cmdline..." ;;
	*)
		if [ -x /usr/sbin/soundconf ]; then
			echo "Using sound kernel module $DRIVER..."
			/usr/sbin/soundconf -M $DRIVER
		fi ;;
	esac
# Sound card may already be detected by PCI-detect.
elif [ -d /proc/asound ]; then
	# Restore sound config for installed system.
	if [ -s /etc/asound.state ]; then
		echo -n "Restoring last alsa configuration..."
		alsactl restore
		status
	else
		/usr/sbin/setmixer
	fi
	# Start soundconf to config driver and load module for Live mode
	# if not yet detected.
	/usr/bin/amixer >/dev/null || /usr/sbin/soundconf
else
	echo "Unable to configure sound card."
fi

# Xorg auto configuration.
if [ ! -s /etc/X11/xorg.conf -a -x /usr/bin/Xorg ]; then
	echo "Configuring Xorg..."
	# $HOME is not yet set.
	HOME=/root
	Xorg -configure
	mv -f /root/xorg.conf.new /etc/X11/xorg.conf
	sed -i 's|/usr/bin/Xvesa|/usr/bin/Xorg|' /etc/slim.conf
	sed -i s/"^xserver_arguments"/'\#xserver_arguments'/ /etc/slim.conf
	tazx config-xorg
fi
if [ "$VESA" = "yes" ]; then
	if [ -f /etc/X11/xorg.conf.vesa ]; then
		HOME=/root
		cp -f /etc/X11/xorg.conf.vesa /etc/X11/xorg.conf
		sed -i 's|/usr/bin/Xvesa|/usr/bin/Xorg|' /etc/slim.conf
		sed -i s/"^xserver_arguments"/'\#xserver_arguments'/ /etc/slim.conf
		tazx config-xorg
	fi
fi
# Screen size config for slim/Xvesa (last config dialog before login).
#
# NOTE: Xvesa is unmaintained, package will be removed and all related
# code cleaned 
#
if [ ! -s /etc/X11/screen.conf -a -x /usr/bin/Xvesa ]; then
	# $HOME is not yet set.
	HOME=/root
	if [ -n "$XARG" ]; then
		# Add an extra argument to xserver_arguments (xarg=-2button)
		sed -i "s| -screen|$XARG -screen|" /etc/slim.conf
	fi
	if [ -n "$SCREEN" ]; then
		case "$SCREEN" in
			text)
				# Disable X.
				echo -n "Disabling X login manager: slim..."
				. /etc/rcS.conf
				RUN_DAEMONS=`echo $RUN_DAEMONS | sed s/' slim'/''/`
				sed -i s/"RUN_DAEMONS.*"/"RUN_DAEMONS=\"$RUN_DAEMONS\"/" /etc/rcS.conf
				status ;;
			auto)
				# Auto detect screen resolution.
				export NEW_SCREEN=`Xvesa -listmodes 2>&1 | grep ^0x | \
					awk '{ printf "%s %s\n",$2 }' \
					| sort -nr | grep x[1-2][4-6] | head -n 1`
				tazx `cat /etc/X11/wm.default` ;;
			1024x600*|800x480*)
				set -- $(echo $SCREEN | sed 's/x/ /g')
				915resolution -l 2>/dev/null | \
				grep " ${1}x" | awk -v h=$1 -v v=$2 \
				'END {system("915resolution " $2 " " h " " v)}'
				# Use specified screen resolution.
				export NEW_SCREEN=$SCREEN
				tazx `cat /etc/X11/wm.default` ;;
			*)
				# Use specified screen resolution.
				export NEW_SCREEN=$SCREEN
				tazx `cat /etc/X11/wm.default` ;;
		esac
	else
		tazx `cat /etc/X11/wm.default`
	fi
fi
