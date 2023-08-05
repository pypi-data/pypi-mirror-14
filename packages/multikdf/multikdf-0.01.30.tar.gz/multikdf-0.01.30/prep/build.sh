#!/bin/sh
if [ -z "$1" ]; then
	echo "This file is intended to used only during package installation"
	exit 0
fi
cd $1
make prep
