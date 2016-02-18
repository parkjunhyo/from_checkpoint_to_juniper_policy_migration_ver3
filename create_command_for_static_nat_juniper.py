#! /usr/bin/env python

import sys
from Routing_information import Routing_information

read_file_name = "./static_nat_address.txt"
output_file_name = "./static_nat_address_juniper_command.txt"

f = open(read_file_name,"r")
contents = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()

juniper_inside = "set security nat static rule-set %s rule %s match destination-address %s"
juniper_outside = "set security nat static rule-set %s rule %s then static-nat prefix %s"

rule_set_name = Routing_information.juniper_static_nat_rule_set_name

for content_in in contents:

   content_list = content_in.split("\t")
   policy_public = content_list[0]
   policy_private = content_list[1].strip()
   policy_rule_name = "_".join(policy_public.split("."))

   f = open(output_file_name,"a")

   in_msg = juniper_inside % (rule_set_name,policy_rule_name,policy_public+"/32")
   f.write(in_msg+"\n")

   in_msg = juniper_outside % (rule_set_name,policy_rule_name,policy_private+"/32")
   f.write(in_msg+"\n")

   f.close()
