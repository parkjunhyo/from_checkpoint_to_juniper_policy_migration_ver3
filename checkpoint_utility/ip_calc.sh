#! /usr/bin/env bash

ip_address=$1
netmask=$2

ipcalc $ip_address $netmask > result.ip_calc
