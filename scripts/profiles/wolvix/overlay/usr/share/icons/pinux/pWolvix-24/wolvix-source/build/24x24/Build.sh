#!/bin/sh

if test ! -d cursors;
then mkdir cursors
else
rm -rf cursors
mkdir cursors
fi



########### Build cursors

xcursorgen AppStarting.conf	cursors/AppStarting
xcursorgen Wait.conf		cursors/Wait

cd cursors



########### Create copies and symlinks

#---------- AppStarting
cp AppStarting			left_ptr_watch
cp -s left_ptr_watch	08e8e1c95fe2fc01f976f1e063a24ccd
cp -s left_ptr_watch	3ecb610c1bf2410f44200f48c40d3599
rm -f AppStarting

#---------- Wait
cp Wait					watch
rm -f Wait



########### Done!
echo "Done!"
