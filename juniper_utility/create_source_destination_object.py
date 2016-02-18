#! /usr/bin/env python

file_names = ["./source.match_zone","./destination.match_zone"]
output_file_name = "./command_to_create_source_destination_object.txt"

f = open(output_file_name,"w")
f.close()


duplicated_info = []
for file_name in file_names:

   f = open(file_name, "r")
   contents_in_file = f.readlines()
   f.close()


   for content_in_file in contents_in_file:
      
      [ policy_no, zone_name, _information_ ] =content_in_file.strip().split("\t")
      temp_obj_name = "_".join([zone_name, _information_])

      if temp_obj_name not in duplicated_info:
        duplicated_info.append(temp_obj_name)
        f = open(output_file_name,"a")
        cli_command = "set security zones security-zone %s address-book address %s %s\n" % (zone_name, _information_, _information_)
        f.write(cli_command)
        f.close()
