#! /usr/bin/env python

import os
import random

file_names = ["./source.match_zone","./destination.match_zone"]
output_file_name = "./command_to_create_source_destination_object.txt"

f = open(output_file_name,"w")
f.close()


duplicated_info = []
zonename_list = []

temp_random_filename = "./"+str(random.random()).split(".")[1]

for file_name in file_names:

   f = open(file_name, "r")
   contents_in_file = f.readlines()
   f.close()


   for content_in_file in contents_in_file:
      
      [ policy_no, zone_name, _information_ ] =content_in_file.strip().split("\t")

      os_cmd = "./valid_ip_check.sh %s %s" % (_information_, temp_random_filename)
      os.system(os_cmd)
      fr = open(temp_random_filename,"r")
      fr_contents = fr.readlines()
      fr.close()
      os.system("rm -rf temp_random_filename")
      if len(fr_contents) == 0:
        valid_ip = _information_
      else:
        valid_ip = fr_contents[0].strip()

      if zone_name not in zonename_list:
        zonename_list.append(zone_name)
      temp_obj_name = "_".join([zone_name, valid_ip])

      if temp_obj_name not in duplicated_info:
        duplicated_info.append(temp_obj_name)
        f = open(output_file_name,"a")
        cli_command = "set security zones security-zone %s address-book address %s %s\n" % (zone_name, valid_ip, valid_ip)
        f.write(cli_command)
        f.close()



# zone create
f = open("./command_to_create_zone_define.txt","a")
for _zone_ in zonename_list:
   cli_command = "set security zones security-zone %s\n" % (_zone_)
   f.write(cli_command)
f.close()

