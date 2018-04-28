#!/bin/bash
echo $1
if ! type "$1" > /dev/null; then
	exit 0
fi
exit 1
