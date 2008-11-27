#!/bin/bash

. /etc/rc.conf
. /etc/rc.d/functions
. /etc/rc.d/functions.d/cmdline 
. /etc/rc.d/functions.d/splash

disable_splash() {
	if /bin/grep -q " splash" /proc/cmdline; then
		splash_exit
		sleep 0.5
		/usr/bin/chvt 1
	else
		/bin/true
	fi
}

# PREEMPTIVE CLEAN UP AT FIRST
preemptive_cleanup() {
		rm -rf /etc/X11/xorg.con* &>/dev/null
		rm -rf /xorg.* &>/dev/null
}

# GENERATE INITIAL CONFIG
generate_initial_config() {
		printhl2 "Your screen will probably flicker for a moment, dont panic :)"
		sleep 2
		LANG=C /usr/bin/Xorg -configure -novtswitch :1 > /tmp/xorg_detection.log 2>&1
		mv /xorg.conf.new /etc/X11/xorg.conf.plain
}

# CHECK THE DETECTED DRIVER
output_initial_detected_driver() {
		XORG_DRIVERS="amd apm ark ati chips cirrus glint i128 i740 intel mach64 mga neomagic nv r128 radeon radeonhd rendition s3 s3virge savage siliconmotion sis sisusb tdfx trident tseng v4l voodoo ztv fbdev vesa vga vmware"

		for i in $XORG_DRIVERS ; do
			if grep -q ${i} /etc/X11/xorg.conf.plain ; then
			USED_DRIVER=$i
			fi
		done

		printhl "Detected video device: $USED_DRIVER"
}

# DETECT RESOLUTIONS FROM KERNEL COMMANDLINE AND PUT IT INTO XORG.CONF
setup_resolution() {
		# at first, add the sane default (tm)
		sed -i '/Viewport/ a\                Modes "default"' /etc/X11/xorg.conf.plain

		# now check if the user has specified a resolution on kernel commandline, and apply it
		XRES=`get_xres`
			[ -n "$XRES" ] || XRES="default"

		case "$XRES" in
			640x480)
				sed -i 's/^.*Modes.*/                Modes      "640x480"/' /etc/X11/xorg.conf.plain
			;;
			800x600)
				sed -i 's/^.*Modes.*/                Modes      "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1024x768)
				sed -i 's/^.*Modes.*/                Modes      "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1152x864)
				sed -i 's/^.*Modes.*/                Modes      "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1280x1024)
				sed -i 's/^.*Modes.*/                Modes      "1280x1024" "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1400x1050)
				sed -i 's/^.*Modes.*/                Modes      "1400x1050" "1280x1024" "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1600x1200)
				sed -i 's/^.*Modes.*/                Modes      "1600x1200" "1400x1050" "1280x1024" "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1680x1050)
				sed -i 's/^.*Modes.*/                Modes      "1680x1050" "1600x1200" "1400x1050" "1280x1024" "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1280x800)
				sed -i 's/^.*Modes.*/                Modes      "1280x800" "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			1280x960)
				sed -i 's/^.*Modes.*/                Modes      "1280x960" "1280x800" "1152x864" "1024x768" "800x600" "640x480"/' /etc/X11/xorg.conf.plain
			;;
			default)
				/bin/true
				# we do nothing (tm)
				# default has already been applied...
			;;
			*)
				/bin/true
				# we do nothing (tm)
				# default has already been applied...
			;;
		esac
}

# DETECT COLOR DEPTH FROM KERNEL COMMANDLINE
setup_depth() {
XDEPTH=`get_xdepth`
		[ -n "$XDEPTH" ] || XDEPTH="24"

		case "$XDEPTH" in
			8)
			COLORDEPTH="DefaultDepth $XDEPTH\n\tSubSection \"Display\""
			sed -i 1,/'SubSection "Display"'/s/'SubSection "Display"'/"$COLORDEPTH"/ /etc/X11/xorg.conf.plain
			;;
			15)
			COLORDEPTH="DefaultDepth $XDEPTH\n\tSubSection \"Display\""
			sed -i 1,/'SubSection "Display"'/s/'SubSection "Display"'/"$COLORDEPTH"/ /etc/X11/xorg.conf.plain
			;;
			16)
			COLORDEPTH="DefaultDepth $XDEPTH\n\tSubSection \"Display\""
			sed -i 1,/'SubSection "Display"'/s/'SubSection "Display"'/"$COLORDEPTH"/ /etc/X11/xorg.conf.plain
			;;
			24)
			COLORDEPTH="DefaultDepth $XDEPTH\n\tSubSection \"Display\""
			sed -i 1,/'SubSection "Display"'/s/'SubSection "Display"'/"$COLORDEPTH"/ /etc/X11/xorg.conf.plain
			;;
			32)
			COLORDEPTH="DefaultDepth $XDEPTH\n\tSubSection \"Display\""
			sed -i 1,/'SubSection "Display"'/s/'SubSection "Display"'/"$COLORDEPTH"/ /etc/X11/xorg.conf.plain
			;;
		esac
}

# DETECT LANGUAGE FROM KERNEL COMMANDLINE AND PUT IT INTO XORG.CONF...
setup_keyboard_layout() {
		COUNTRY=`get_country`
		[ -n "$COUNTRY" ] || COUNTRY="en"

		case "$COUNTRY" in
			be)
			# Belgian version
			XKEYBOARD="be"
			;;
			bg)
			# Bulgarian version
			XKEYBOARD="bg"
			;;
			cn)
			# Simplified Chinese version
			XKEYBOARD="us"
			;;
			cz)
			# Czech version
			XKEYBOARD="cs"
			;;
			de)
			# German version
			XKEYBOARD="de"
			;;
			dk)
			# Danish version
			XKEYBOARD="dk"
			;;
			en)
			# English version
			XKEYBOARD="en"
			;;
			es)
			# Spanish version
			XKEYBOARD="es"
			;;
			fi)
			# Finnish version
			XKEYBOARD="fi"
			;;
			fr)
			# Francais version
			XKEYBOARD="fr"
			;;
			hu)
			# Hungarian version
			XKEYBOARD="hu"
			;;
			it)
			# German version
			XKEYBOARD="it"
			;;
			ja)
			# Japanese version
			XKEYBOARD="us"
			;;
			nl)
			# Dutch version
			XKEYBOARD="us"
			;;
			no)
			# Norway version
			XKEYBOARD="no"
			;;
			pl)
			# Polish version
			XKEYBOARD="pl"
			;;
			ru)
			# Russian version
			XKEYBOARD="ru"
			;;
			sk)
			# Slovakian version
			XKEYBOARD="sk"
			;;
			sl)
			# Slovenian version
			XKEYBOARD="sl"
			;;
			tr)
			# Turkish version
			XKEYBOARD="tr"
			;;
			uk)
			# British version
			XKEYBOARD="uk"
			;;
			*)
			# American version
			XKEYBOARD="us"
			;;
		esac

		# TODO - hardcoded values here, need to add kernel options
		test -z "$XKBRULES" && XKBRULES="xorg"
		test -z "$XKBMODEL" && XKBMODEL="pc105"

		KEYBOARD_SETTINGS="Option      \"XkbRules\" \"$XKBRULES\"\n\tOption      \"XkbModel\" \"$XKBMODEL\"\n\tOption      \"XkbLayout\" \"$XKEYBOARD\""
		sed -i /'Driver.*"kbd"'/a\ "\\\t$KEYBOARD_SETTINGS" /etc/X11/xorg.conf.plain
}

#
# LETS START
#
disable_splash
preemptive_cleanup
printhl "Detecting video & input hardware"
generate_initial_config
output_initial_detected_driver
setup_resolution
setup_depth
printhl "Configuring input"
setup_keyboard_layout

#
# FINAL TOUCHES
#
cat <<EOF >> /etc/X11/xorg.conf.plain
Section "Extensions"
	Option "Composite" "Enable"
	Option "RENDER" "Enable"
EndSection

EOF

 # prepend the AIGLX option the first occurence of EndSection, which should be in the ServerLayout section, where it belongs
ADD_AIGLX="        Option         \"AIGLX\" \"true\"\n\tEndSection"
sed -i 1,/'EndSection'/s/'EndSection'/"$ADD_AIGLX"/ /etc/X11/xorg.conf.plain

# enable DPMS for the monitor
sed -i /'Section "Monitor"'/,/'EndSection'/s/'EndSection'/"\tOption       \"DPMS\"\nEndSection"/g /etc/X11/xorg.conf.plain

# add some standard device options
sed -i /'Section "Device"'/,/'EndSection'/s/'EndSection'/"\tOption      \"VBERestore\"    \"true\"\nEndSection"/g /etc/X11/xorg.conf.plain
sed -i /'Section "Device"'/,/'EndSection'/s/'EndSection'/"\tOption      \"DRI\"    \"true\"\nEndSection"/g /etc/X11/xorg.conf.plain
sed -i /'Section "Device"'/,/'EndSection'/s/'EndSection'/"\tOption      \"XAANoOffscreenPixmaps\"    \"true\"\nEndSection"/g /etc/X11/xorg.conf.plain

#
# CLEANUP AND APPLY CONFIG
#
mv /etc/X11/xorg.conf.plain /etc/X11/xorg.conf &>/dev/null
