#!/bin/bash

if [ $# -ne 6 ]; then
	echo "usage: $( basename "$0" ) <banner-silent> <banner-verbose> <separator-size> <icon_size> <icon-size-small> <progress-bar-width>" >&2
	exit 1
fi

_banner_silent="$1"
_banner_verbose="$2"
_sep_width="${3%x*}"
_sep_height="${3#*x}"
_icon_size="$4"
_icon_size_small="$5"
_progress_width="$6"

set -e

mkdir -p images
cd images

# make banner images
convert -depth 8 -background none ${_banner_silent} -trim +repage banner.png
convert -background none ${_banner_verbose} banner_2.png

# logo/banner size
l_res="$(
	convert banner.png -identify /dev/null |
	sed -r 's,^.*[[:space:]]([0-9]+x[0-9]+)[[:space:]].*$,\1,'
)"
lw="${l_res%x*}"
lh="${l_res#*x}"

_progress_height=$lh

# make blue separator image
convert -type TrueColorMatte -depth 8 \
	-size ${_sep_width}x${_sep_height} xc:black \
	-fill '#2979a2' -draw \
		"rectangle 1,0 $(( _sep_width - 2 )),${_sep_height}" \
	-fill '#5dbded' -draw \
		"line 0,$(( _sep_height/2 )) ${_sep_width},$(( _sep_height/2 ))" \
	separator.png

# make red separator image
convert -type TrueColorMatte -depth 8 \
	-size ${_sep_width}x${_sep_height} xc:black \
	-fill '#a22929' -draw \
		"rectangle 1,0 $(( _sep_width - 2 )),3" \
	-fill '#ed5d5d' -draw \
		"line 0,$(( _sep_height/2 )) ${_sep_width},$(( _sep_height/2 ))" \
	separator-red.png

# make dummy daemon icon
convert -type TrueColorMatte -depth 8 -size 1x1 xc:transparent dummy.png

# make background icon covers
convert -type TrueColorMatte -depth 8 -size ${_icon_size}x${_icon_size} \
	xc:black -fill black -draw 'color 0,0 reset' \
	cover.png
convert -type TrueColorMatte -depth 8 -size ${_icon_size_small}x${_icon_size_small} \
	xc:black -fill black -draw 'color 0,0 reset' \
	cover-small.png

# make animated progress bar background - progress-bkgd.mng
rm -f spinner-*.png
stripe_height=2
#increment=$(( _progress_height/12 )) ; [ $increment -gt 1 ] || increment=1
increment=1
digits=$(( ${#_progress_height} + 1 ))
for (( i=_progress_height; i>0; i-=increment )) do
	ii=$i
	while [ ${#ii} -lt $digits ]; do
		ii=0$ii
	done
	convert -type TrueColorMatte -depth 8 \
		-size ${_progress_width}x${_progress_height} xc:black \
		-fill '#0a3f5a' -draw "rectangle 0,0 ${_progress_width},${_progress_height}" \
		-fill '#000000' -draw "polygon $(( _progress_width/3   )),$((_progress_height-i                   )) ${_progress_width},$((_progress_height-i-stripe_height/2                   )) ${_progress_width},$((_progress_height-i+stripe_height/2                   ))" \
		-fill '#000000' -draw "polygon $(( _progress_width*2/3 )),$((_progress_height-i-_progress_height/2))                  0,$((_progress_height-i-stripe_height/2-_progress_height/2))                  0,$((_progress_height-i+stripe_height/2-_progress_height/2))" \
		-fill '#000000' -draw "polygon $(( _progress_width*2/3 )),$((_progress_height-i+_progress_height/2))                  0,$((_progress_height-i-stripe_height/2+_progress_height/2))                  0,$((_progress_height-i+stripe_height/2+_progress_height/2))" \
	spinner-$ii.png
done
convert -delay 1x30 spinner-*.png progress-bkgd.mng

## make simple spinner animation
#_spin_width=7  # odd numbers to get a centered pixel in the middle
#_spin_height=7
#vectors_x=( 100 71   0 -71 -100 -71    0  71 )
#vectors_y=(   0 71 100  71    0 -71 -100 -71 )
#rm -f spinner-*.png
#for i in $(seq 0 3) ; do # half sequence
#	ii=$i ; [ $i -ge 10 ] || ii=0$i
#	convert -type TrueColorMatte -depth 8 \
#		-size ${_spin_width}x${_spin_height} xc:black \
#		-fill '#c0c0c0' -draw "line \
#                     $((  _spin_width*(100-vectors_x[i])/200 )),$(( _spin_height*(100-vectors_y[i])/200 )) \
#                     $((  _spin_width*(100+vectors_x[i])/200 )),$(( _spin_height*(100+vectors_y[i])/200 ))" \
#		spinner-$ii.png
#done
#convert -delay 1x60 spinner-*.png spinner.mng

## make spinner cover
#convert -type TrueColorMatte -depth 8 \
#	-size ${_spin_width}x${_spin_height} xc:black \
#	spinner-black.png
