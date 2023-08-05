#!/bin/sh
if [ -z "$1" ]; then
	echo "This file is intended to used only during package installation"
	exit 0
fi

cd $1
export PLATFORM=$(gcc -dumpmachine | cut -d- -f1)
make -C custom
make -C source
exit 0
