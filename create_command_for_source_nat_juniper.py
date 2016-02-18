#! /usr/bin/env python

import sys
from Routing_information import Routing_information

read_file_name = "./text_type_global_nat_result.txt"
output_file_name = "./source_nat_address_juniper_command.txt"

f = open(read_file_name,"r")
contents = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()

juniper_source = "set security nat source rule-set %s rule %s match source-address %s"
juniper_destination = "set security nat source rule-set %s rule %s match destination-address 0.0.0.0/0"
juniper_pool = "set security nat source rule-set %s rule %s then source-nat pool %s"

juniper_pool_define = "set security nat source pool %s address %s to %s"


rule_set_name = Routing_information.juniper_static_nat_rule_set_name
source_rule_limit = 8

for content_in in contents:
   
   f = open(output_file_name,"a")

   content_list = content_in.split("\t")

   juniper_no = content_list[0]
   juniper_status = content_list[1]
   juniper_inside = content_list[2]
   juniper_source_address = content_list[3]
   juniper_outside = content_list[4]
   juniper_nat_public = content_list[5].strip()

   if juniper_status != "OK":
     continue

   rule_set_name = "from_%s_to_%s" % (juniper_outside,juniper_inside)
   pool_name = "_".join(juniper_nat_public.split("/")[0].split("."))
   in_msg = juniper_pool_define % (pool_name,juniper_nat_public,juniper_nat_public)
   f.write(in_msg+"\n")
   
   source_no_count = 0
   source_address_list = juniper_source_address.split(";")
   for _source_address_ in source_address_list:

      if len(source_address_list) < source_rule_limit:
        rule_name = pool_name
        size_status = 0
      else:
        size_status = 1
        extra_name = str(source_no_count / source_rule_limit)
        rule_name = pool_name+"_"+extra_name
        

      in_msg = juniper_source % (rule_set_name,rule_name,_source_address_)
      f.write(in_msg+"\n")

      last_index_status = 0
      if source_no_count + 1 == len(source_address_list):
        last_index_status = 1

      if size_status == 0:
        if last_index_status:
          in_msg = juniper_destination % (rule_set_name,rule_name)
          f.write(in_msg+"\n")
          in_msg = juniper_pool % (rule_set_name,rule_name,pool_name)
          f.write(in_msg+"\n")
      else:
        if last_index_status:
          in_msg = juniper_destination % (rule_set_name,rule_name)
          f.write(in_msg+"\n")
          in_msg = juniper_pool % (rule_set_name,rule_name,pool_name)
          f.write(in_msg+"\n")
        else:
          if (source_no_count + 1) % source_rule_limit == 0:
            in_msg = juniper_destination % (rule_set_name,rule_name)
            f.write(in_msg+"\n")
            in_msg = juniper_pool % (rule_set_name,rule_name,pool_name)
            f.write(in_msg+"\n")

      source_no_count = source_no_count + 1
      
   f.close()
  
