#! /usr/bin/env bash

searching_object=$1
result_file=$2
searching_filename="./network_objects.gen"

cat $searching_filename | grep -i $searching_object > $result_file
