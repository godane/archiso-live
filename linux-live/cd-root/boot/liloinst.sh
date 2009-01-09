#!/bin/bash
# This script will make almost ANY partition bootable, regardless the filesystem
# used on it. bootinst.sh/.bat is only for FAT filesystems, while this one should
# work everywhere. Moreover it setups a 'slaxchanges' directory to be used for
# persistent changes.

set -e
TARGET=""
MBR=""

# Find out which partition or disk are we using
MYMNT=$(cd -P $(dirname $0) ; pwd)
while [ "$MYMNT" != "" -a "$MYMNT" != "." -a "$MYMNT" != "/" ]; do
   TARGET=$(egrep "[^[:space:]]+[[:space:]]+$MYMNT[[:space:]]+" /proc/mounts | cut -d " " -f 1)
   if [ "$TARGET" != "" ]; then break; fi
   MYMNT=$(dirname "$MYMNT")
done

if [ "$TARGET" = "" ]; then
   echo "Can't find device to install to."
   echo "Make sure you run this script from a mounted device."
   exit 1
fi

if [ "$(cat /proc/mounts | grep "^$TARGET" | grep noexec)" ]; then
   echo "The disk $TARGET is mounted with noexec parameter, trying to remount..."
   mount -o remount,exec "$TARGET"
fi

MBR=$(echo "$TARGET" | sed -r "s/[0-9]+\$//g")
NUM=${TARGET:${#MBR}}
cd "$MYMNT"

# only partition is allowed, not the whole disk
if [ "$MBR" = "$TARGET" ]; then
   echo Error: You must install your system to a partition, not the whole disk
   exit 1
fi

clear
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
echo "                        Welcome to Slax boot installer                         "
echo "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
echo
echo "This installer will setup disk $MBR to boot only Slax from $TARGET."
echo "Warning! Master boot record (MBR) of $MBR will be overwritten."
echo "If you use $MBR to boot any existing operating system, it will not work"
echo "anymore. Only Slax will boot from this device. Be careful!"
echo
echo "Press any key to continue, or Ctrl+C to abort..."
read junk
clear

echo "Flushing filesystem buffers, this may take a while..."
sync

mkdir -p $MYMNT/slaxchanges
if [ $? -ne 0 ]; then
   echo "Make sure to mount the partition read-write." >&2
   exit 5
fi

cat << ENDOFTEXT >$MYMNT/boot/lilo.conf
boot=$MBR
prompt
timeout=40
lba32
compact
change-rules
reset
install=text
image=$MYMNT/boot/vmlinuz
initrd=$MYMNT/boot/initrd.gz
label=Slax
root=/dev/ram0
read-write
append = "ramdisk_size=6666 changes=slaxchanges"
ENDOFTEXT

echo Updating MBR to setup boot record...
boot/syslinux/lilo -C $MYMNT/boot/lilo.conf -S $MYMNT/boot/ -m $MYMNT/boot/lilo.map
echo "Disk $MBR should be bootable now. Installation finished."

echo
echo "Read the information above and then press any key to exit..."
read junk
