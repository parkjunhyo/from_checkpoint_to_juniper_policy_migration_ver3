#! /usr/bin/env bash

if [ $# -ne 2 ]
then
 exit
fi

ipcalc $1 | grep -i 'network' | awk '{print $2}' > $2



