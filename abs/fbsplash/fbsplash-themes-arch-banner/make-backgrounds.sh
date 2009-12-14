#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $( basename "$0" ) <width>x<height>" >&2
	exit 1
fi

_size="$1"
_width=${_size%x*}
_height=${_size#*x}

set -e

mkdir -p images
cd images

convert -type TrueColorMatte -depth 8 -size $_size xc:black -fill black -draw 'color 0,0 reset' \
	silent-$_size.png
convert -type TrueColorMatte -depth 8 -size $_size xc:black -fill '#051e2a' -draw 'color 0,0 reset' \
	backgnd-$_size.png
composite -geometry +$(( _width - 640 ))+$(( _height - 200 )) \
	banner_2.png backgnd-$_size.png \
	verbose-$_size.png

