#!/bin/bash

# same as in cache-links
daemons=(
	acpid
	alsa
	cups
	samba
	mysqld
	netfs
	nfsd
	sensors
	smartd
)

_logo=images/banner.png

msg() {
	echo "$@" >&2
}

msg "$0" "$@"

usage() {
  msg "Usage: ${0##*/} <name> icons|noicons <screen-size> <icon|banner-file> <separator-width> <seperator-height> <font-file> <font-size> <icon-size> <progress-bar-width>"
  exit 1
}

[ $# -eq 9 ] || usage

_name="$1"
_variant="$2"
_size="$3"
_sep_width="$4"
_sep_height="$5"
_font="$6"
_font_size="$7"
_icon_size="$8"
_progress_width="$9"

case "$_variant" in
	noicons ) use_icons=0 ;;
	icons   ) use_icons=1 ;;
	*       ) usage ;;
esac

if [ "${_logo# *}" != "${_logo}" -o \
     "${_font# *}" != "${_font}" ]; then
  msg "Blanks not allowed in filepaths."
  exit 1
fi

msg "cwd: $( pwd )"

for f in "$_logo" "$_font" ; do
	if ! [ -f $f ]; then
		msg "File not found: '$f'"
		exit 1
	fi
done

set -u

mkdir -p "${_name}"

# screen size
x="${_size%x*}"
y="${_size#*x}"

msg "Screen size is $_size"

# fixed point for placement
xf=$(( x / 2 ))
yf=$(( y / 2 ))

if ! [ -e "${_logo}" ]; then
  msg "File not found: '${_logo}'"
  exit 1
fi

# text font size
tf=${_font_size}

# estimated height of 1000 lines of text
th_1000=$(( 15600 * tf / 12 ))

# logo/banner size
l_res="$(
	convert "${_logo}" -identify /dev/null |
	sed -r 's,^.*[[:space:]]([0-9]+x[0-9]+)[[:space:]].*$,\1,'
)"
lw="${l_res%x*}"
lh="${l_res#*x}"

# progress size
pw=$_progress_width
ph=$lh

# main area (logo + progress)
mw=$(( lw + 20 + pw ))

# separator 
sx=$(( xf - _sep_width/2 ))
sy=$(( yf - _sep_height/2 ))

# main message text heigth
th=$(( th_1000/1000 ))

# status bar
sbh=$(( th + 20 ))
sbx=$(( xf - mw/2 ))
sby=$(( sy - _sep_height/2 - sbh ))

# main message text position
tx=$(( sbx + 15 ))
ty=$(( sby + sbh/2 - th/2 ))

# logo/banner position
lx=$(( xf - mw/2 ))
ly=$(( sby - lh  ))

# corners of progress bar
ptl="$(( xf + mw/2 - pw   )) $(( ly      ))" # progress top left corner
ptr="$(( xf + mw/2 - 1    )) $(( ly      ))" # progress top right corner

pbl="$(( xf + mw/2 - pw   )) $(( ly + lh ))" # progress bottom left corner
pbr="$(( xf + mw/2 - 1    )) $(( ly + lh ))" # progress bottom right corner

## icon bar
if [ ${use_icons} = 1 ]; then
	iy=$(( sy + 20 ))  
	is=${_icon_size}
	msg "Using icons"
else
	iy=$(( sy + _sep_height/2 ))
	is=0
	msg "NOT using icons"
fi
iw=$(( _sep_width - is ))
ix=$(( xf - iw/2 ))

# message log
ox=$(( tx      ))
oy=$(( iy + is + 20 ))
#oy=$(( iy + is + 10 ))
of=${_font_size}
# estimated height of 1000 lines of text
oh_1000=$(( 15600 * of / 12 ))

msg "Message log y is ${oy}"

# number of message log lines
ol=$(( 1000 * ( y - oy - 10 ) / oh_1000 ))

msg "Number of message lines is ${ol}"

# args: <event> <daemon>
separator_red()
{
	local file
	
	file="images/separator-red.png"
	if ! [ -f "${file}" ]; then
		msg "File not found: '${file}'"
		exit 1
	fi
	echo icon "${file}" $sx $sy ${1} ${2}
}

# arg: start|stop
icon_bar()
{
	local i icon_x
	local j events
	local icon_num=0
	
	for (( i=0 ; i<"${#daemons[@]}" ; i++ )) do
		
		icon_x=$((ix + icon_num*is*3/2 ))
		stat_icon_x=$((ix + icon_num*is*3/2 + is/2 ))
		
		if [ ${icon_x} -gt $(( ix + iw - is )) ]; then
			msg "Icon bar width exceeded - to many icons !"
			exit 1
		fi
		
		if [ ${1} = stop ]; then
			echo icon /lib/splash/cache/arch-banner-icons/${daemons[i]}.init $icon_x $iy
		fi
		
		case ${1} in
			( start ) events="svc_start svc_started svc_start_failed" ;;
#			( stop  ) events="svc_started svc_stop svc_stop_failed" ;;
			( stop  ) events="" ;;
		esac
		for j in ${events} ; do
			echo icon /lib/splash/cache/arch-banner-icons/${daemons[i]} $icon_x $iy $j ${daemons[i]}
		done
		
		echo icon /lib/splash/cache/arch-banner-icons/${1} $stat_icon_x $iy svc_${1}        ${daemons[i]}
		echo icon /lib/splash/cache/arch-banner-icons/fail $stat_icon_x $iy svc_${1}_failed ${daemons[i]}
		echo
		
		if [ ${1} = stop ]; then
			echo icon images/cover.png       $icon_x $iy svc_stopped ${daemons[i]}
			echo icon images/cover-small.png $stat_icon_x $iy svc_stopped ${daemons[i]}
			echo
		fi
		
		(( icon_num++ ))
	done
}

{
	cat <<EOF

pic=images/verbose-$_size.png
bgcolor=0
tx=0
ty=0
tw=$x
th=$y

silentpic=images/silent-$_size.png

icon $_logo $lx $ly

text_font=$_font
text_size=$tf
text_x=$tx
text_y=$ty
text_color=#e0e0e0

icon images/separator.png $sx $sy

# This type is used by fbcondecor_helper in initcpio
# and by fbcondecor_ctl (patched version)
<type other>
</type>

<type bootup>
  icon /lib/splash/cache/arch-banner-icons/fbsplash-dummy.init $sx $sy
  
#  box silent       $ptl $pbr #0a3f5a
  anim loop  images/progress-bkgd.mng $ptl
  box silent inter $pbl $pbr #5dbded #106691 #5dbded #106691
  box silent       $ptl $pbr #5dbded #106691 #5dbded #106691

EOF

	{
		separator_red svc_start_failed fbsplash-dummy
		echo
		if [ ${use_icons} = 1 ]; then
			icon_bar start
		fi
	} | sed 's,^,  ,'

	cat <<EOF
</type>

<type suspend>
  box silent       $ptl $pbr #0a3f5a
  box silent inter $ptl $pbr #5dbded #106691 #5dbded #106691
  box silent       $pbl $pbr #5dbded #106691 #5dbded #106691
</type>

<type reboot shutdown>
  icon /lib/splash/cache/arch-banner-icons/fbsplash-dummy.init $sx $sy

  box silent       $ptl $pbr #0a3f5a
  box silent inter $ptl $pbr #5dbded #106691 #5dbded #106691
  box silent       $pbl $pbr #5dbded #106691 #5dbded #106691

EOF

	{
		separator_red svc_stop_failed fbsplash-dummy
		echo
		if [ ${use_icons} = 1 ]; then
			icon_bar stop
		fi
	} | sed 's,^,  ,'

	cat <<EOF
</type>

# 'tuxoniceui_fbsplash' (version 1.0) doesn't know anything about types.
# It seems to show allways simply the last item defined on top.
# With this one at the end we allways get an upward growing progress
# whether suspend or resume it done.
<type resume>
  box silent       $ptl $pbr #0a3f5a
  box silent inter $pbl $pbr #5dbded #106691 #5dbded #106691
  box silent       $ptl $pbr #5dbded #106691 #5dbded #106691
</type>

EOF

	if [ $ol -lt 3 ]; then
	  msg " NOT including message log."
	else

	cat <<EOF
log_lines=$ol
log_cols=80
<textbox>
  text silent $_font $of $ox $oy #e0e0e0 msglog
</textbox>

EOF

	fi

} > "${_name}"/${_size}.cfg
