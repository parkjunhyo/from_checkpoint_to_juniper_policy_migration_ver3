#! /usr/bin/env bash

html_dir="/var/www/html/juniper"

function moving {
 if [ -f $1 ]
 then
  mv $1 $2
 fi
}

if [ -d $html_dir ]
then
 rm -rf $html_dir
fi

mkdir $html_dir
chmod 777 $html_dir

file_name="./juniper_type_result.txt"
moving $file_name $html_dir

file_name="./text_type_result.txt"
moving $file_name $html_dir

file_name="./result_global_nat_match.txt"
moving $file_name $html_dir

file_name="./text_type__global_nat_result.txt"
moving $file_name $html_dir

file_name="./static_nat_address.txt"
moving $file_name $html_dir

file_name="./juniper_policy.command"
moving $file_name $html_dir

