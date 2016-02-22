#! /usr/bin/env python

import re

file_names = "./text_type_global_nat_result.txt"
output_file_name = "./command_to_create_global_nat.txt"

f = open(file_names,"r")
contents_in_file = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()


juniper_global_nat_option_from = "set security nat source rule-set %s from zone %s\n"
juniper_global_nat_option_to = "set security nat source rule-set %s to %s\n"

juniper_source = "set security nat source rule-set %s rule %s match source-address %s\n"
juniper_destination = "set security nat source rule-set %s rule %s match destination-address 0.0.0.0/0\n"
juniper_pool = "set security nat source rule-set %s rule %s then source-nat pool %s\n"

juniper_pool_define = "set security nat source pool %s address %s to %s\n"
source_count_limit_in_pool = 6

# find rule set
zone_names_list = []
for content_in_file in contents_in_file:
   [ _policy_number_, _status_, _from_zone_, _source_objects_, _to_zone_, _destination_objects_ ] = content_in_file.strip().split("\t")
   for _zone_ in [ _from_zone_, _to_zone_]:
      if _zone_ not in zone_names_list:
        zone_names_list.append(_zone_)
duplicated_check = []
f = open(output_file_name,"a")
f.write("---------------------------deine rule set--------------------------\n")
for _fromzone_ in zone_names_list:
   for _tozone_ in zone_names_list:
      if _fromzone_ != _tozone_:
        global_nat_rule_set_name = "snat_from_%s_to_%s" % (_fromzone_,_tozone_)
        if global_nat_rule_set_name not in duplicated_check:
          duplicated_check.append(global_nat_rule_set_name)
          cli_command = juniper_global_nat_option_from % (global_nat_rule_set_name,_fromzone_)
          f.write(cli_command)
          cli_command = juniper_global_nat_option_to % (global_nat_rule_set_name,_tozone_)
          f.write(cli_command)
f.close()

# pool
duplicated_check = []
f = open(output_file_name,"a")
f.write("-----------------------------define pool-----------------------\n")
for content_in_file in contents_in_file:
   [ _policy_number_, _status_, _from_zone_, _source_objects_, _nat_ip_match_zone_, _nat_ip_ ] = content_in_file.strip().split("\t")
   if _nat_ip_ != "0.0.0.0/0":
     pool_name = "_".join(_nat_ip_.strip().split("/")[0].split("."))
     if pool_name not in duplicated_check:
       duplicated_check.append(pool_name)
       cli_command = juniper_pool_define % (pool_name, _nat_ip_, _nat_ip_)
       f.write(cli_command)
f.close()


# global_nat
for content_in_file in contents_in_file:
   
   [ _policy_number_, _status_, _from_zone_, _source_objects_, _nat_ip_match_zone_, _nat_ip_ ] = content_in_file.strip().split("\t")
   if _status_ != "OK":
     continue

   # rule_set_name
   global_nat_rule_set_name = "snat_from_%s_to_%s" % (_from_zone_, _nat_ip_match_zone_ )
   # source and destination
   added_name_info = _from_zone_+_nat_ip_match_zone_
   _p_name_ = "_".join(_nat_ip_.strip().split("/")[0].split("."))
   common_pool_name = "_".join(_nat_ip_.strip().split("/")[0].split("."))+"_"+added_name_info

   _source_ip_addr_ = _source_objects_.strip().split(";")
   rule_name = ""
   f = open(output_file_name,"a")
   f.write("-----------------------rule set : %s , pool : %s ------------------------------\n" % (global_nat_rule_set_name, common_pool_name))
   src_counter = 0
   for _src_ip_ in _source_ip_addr_:
      rule_name = common_pool_name + "_" + str(int(src_counter / source_count_limit_in_pool))
      cli_command = juniper_source % (global_nat_rule_set_name, rule_name, _src_ip_)
      f.write(cli_command)
      last_status = 0
      if (src_counter + 1) == len(_source_ip_addr_):
        last_status = 1

      if (src_counter + 1) % source_count_limit_in_pool == 0 and not last_status:
        cli_command = juniper_destination % (global_nat_rule_set_name, rule_name)
        f.write(cli_command)
        cli_command = juniper_pool % (global_nat_rule_set_name, rule_name, _p_name_) 
        f.write(cli_command)
        f.write("\n")
      if last_status:
        cli_command = juniper_destination % (global_nat_rule_set_name, rule_name)
        f.write(cli_command)
        cli_command = juniper_pool % (global_nat_rule_set_name, rule_name, _p_name_)
        f.write(cli_command)
        f.write("\n")
      src_counter = src_counter + 1

   f.close()
         
