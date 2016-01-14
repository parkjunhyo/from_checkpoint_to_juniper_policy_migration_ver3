#! /usr/bin/env bash

ip_address=$1
netmask=$2
result_file=$3

ipcalc $ip_address $netmask | grep -i network | awk -F[" "] '{print $4}' > $result_file
