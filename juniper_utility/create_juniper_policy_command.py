#! /usr/bin/env python

import re
import os
import random

file_names = "./text_type_result.txt"
output_file_name = "./command_to_create_juniper_policy.txt"

f = open(file_names,"r")
contents_in_file = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()


juniper_source_command = "set security policies from-zone %s to-zone %s policy %s match source-address %s\n"
juniper_destination_command = "set security policies from-zone %s to-zone %s policy %s match destination-address %s\n"
juniper_application_command = "set security policies from-zone %s to-zone %s policy %s match application %s\n"
juniper_permit_command = "set security policies from-zone %s to-zone %s policy %s then permit\n"
juniper_log_command = "set security policies from-zone %s to-zone %s policy %s then log session-close\n"
juniper_comment = "set security policies from-zone %s to-zone %s policy %s description \"%s\"\n"

temp_random_filename = "./"+str(random.random()).split(".")[1]

for content_in_file in contents_in_file:
 
   [ _sequence_, _status_, _from_zone_, _source_ip_, _to_zone_, _destination_ip_, _service_, _comments_ ] = content_in_file.strip().split("\t")

   f = open(output_file_name,"a")

   # policy name
   policy_name = "%s_%s%s" % (_sequence_,_from_zone_,_to_zone_)
   # f.write("------------------------------------ %s [ %s ] ----------------------------------\n" % (_sequence_, policy_name))
   f.write("\n")

   # source
   sip_list = _source_ip_.strip().split(";")
   for sip in sip_list:
      if sip == "0.0.0.0/0":
        cli_command = juniper_source_command % (_from_zone_, _to_zone_, policy_name, "any")
      else:
        os_cmd = "./valid_ip_check.sh %s %s" % (sip, temp_random_filename)
        os.system(os_cmd)
        fr = open(temp_random_filename,"r")
        fr_contents = fr.readlines()
        fr.close()
        os.system("rm -rf temp_random_filename")
        if len(fr_contents) == 0:
          cli_command = juniper_source_command % (_from_zone_, _to_zone_, policy_name, sip)
        else:
          valid_ip = fr_contents[0].strip()
          cli_command = juniper_source_command % (_from_zone_, _to_zone_, policy_name, valid_ip)
      f.write(cli_command)

   # destination
   dip_list = _destination_ip_.strip().split(";")
   for dip in dip_list:
      if dip == "0.0.0.0/0":
        cli_command = juniper_destination_command % (_from_zone_, _to_zone_, policy_name, "any")
      else:
        os_cmd = "./valid_ip_check.sh %s %s" % (dip, temp_random_filename)
        os.system(os_cmd)
        fr = open(temp_random_filename,"r")
        fr_contents = fr.readlines()
        fr.close()
        os.system("rm -rf temp_random_filename")
        if len(fr_contents) == 0:
          cli_command = juniper_destination_command % (_from_zone_, _to_zone_, policy_name, dip)
        else:
          valid_ip = fr_contents[0].strip()
          cli_command = juniper_destination_command % (_from_zone_, _to_zone_, policy_name, valid_ip)
      f.write(cli_command)
   
   # application
   app_list = _service_.strip().split(";")
   for app in app_list:
      if app.lower() == "any":
        cli_command = juniper_application_command % (_from_zone_, _to_zone_, policy_name, "any")  
      elif re.search("icmp", app.lower()):
        cli_command = juniper_application_command % (_from_zone_, _to_zone_, policy_name, "junos-icmp-all")
      elif app.lower() == "tcp:21":
        cli_command = juniper_application_command % (_from_zone_, _to_zone_, policy_name, "junos-ftp")
      else:
        [app_proto,app_port] = app.strip().split(":")
        if re.search("-",app_port):
          application_port_name = "%s_%s_%s" % (app_proto.upper(), app_port.split("-")[0], app_port.split("-")[1]) 
        else:
          application_port_name = "%s_%s" % (app_proto.upper(), app_port) 
        cli_command = juniper_application_command % (_from_zone_, _to_zone_, policy_name, application_port_name)  
      f.write(cli_command)
 
   # permit 
   cli_command = juniper_permit_command % (_from_zone_, _to_zone_, policy_name)
   f.write(cli_command)

   # log
   cli_command = juniper_log_command % (_from_zone_, _to_zone_, policy_name)
   f.write(cli_command)

   # comment
   if _comments_ != "-":
     cli_command = juniper_comment % (_from_zone_, _to_zone_, policy_name, _comments_) 
     f.write(cli_command)
    
   f.close()
