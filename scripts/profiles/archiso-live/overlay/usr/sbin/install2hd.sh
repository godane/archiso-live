#!/bin/sh

if [ "$1" = "" ]; then
	echo "$0 /path/to/harddrive"
	exit 1
fi

if [ ! -d "$1" ]; then
	echo "$1 is not a folder."
	exit 1
fi

mkinitcpio -g /boot/kernel26.img

error () { echo -e "\033[1;31;40m!!! \033[1;37;40m$@\033[1;0m"; }
warn ()  { echo -e "\033[1;33;40m*** \033[1;37;40m$@\033[1;0m"; }
info () { echo -e "\033[1;32;40m>>> \033[1;37;40m$@\033[1;0m"; }

info "Setting up folders in $1"
mkdir -p $1/sys
mkdir -p $1/proc
mkdir -p $1/mnt
mkdir -p $1/tmp
mkdir -p $1/dev
mkdir -p $1/usr
mknod $1/dev/console c 5 1 >/dev/null
mknod $1/dev/null c 1 3 >/dev/null
mknod $1/dev/zero c 1 5 >/dev/null
chmod -R 1777 $1/tmp
mkdir -p /media/{cd,dvd,fl}
touch /media/.hal-mtab

info "Installing /bin to $1"
cp -af /bin $1

info "Installing /boot to $1"
cp -af /boot $1

info "Installing /etc to $1"
cp -af /etc $1

info "Installing /root to $1"
cp -af /root $1

info "Installing /sbin to $1"
cp -af /sbin $1

info "Installing /srv to $1"
cp -af /srv $1

info "Installing /lib to $1"
cp -af /lib $1

info "Installing /opt to $1"
cp -af /opt $1

info "Installing /home to $1"
cp -af /home $1

for dir in $(ls -A /usr); do
info "Installing /usr/$dir to $1"
cp -af /usr/$dir $1/usr
done

info "Installing /var to $1"
cp -af /var $1

info "Copying grub files to /boot/grub"
cp -r /usr/lib/grub/i386-pc/* $1/boot/grub
