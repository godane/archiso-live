#!/bin/sh
#AUFS2VERSION=""
#KERNELVERSION=2.6.33
GITSNAPSHOT=20100224
# aufs2 (no -xx) for the latest -rc version.
if [ ! -d aufs2-util.git/.git ]; then
	git clone http://git.c3sl.ufpr.br/pub/scm/aufs/aufs2-util.git aufs2-util.git
else
	git pull
fi
cd aufs2-util.git
#git checkout origin/aufs2${AUFS2VERSION}
#*** apply "aufs2-base.patch" and "aufs2-standalone.patch" to your kernel source files.
cd ..
rm -rf aufs2-util-${GITSNAPSHOT}
cp -a aufs2-util.git aufs2-util-${GITSNAPSHOT}
tar -czf aufs2-util-${GITSNAPSHOT}.tar.gz --exclude=.git aufs2-util-${GITSNAPSHOT}
