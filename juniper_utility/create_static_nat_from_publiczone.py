#! /usr/bin/env python

import re

file_names = "./static_nat_address.txt"
output_file_name = "./command_to_create_static_nat_from_publiczone.txt"

f = open(file_names,"r")
contents_in_file = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()

static_nat_rule_set_name = "static_from_pub"

juniper_public_nat = "set security nat static rule-set %s from zone pub\n"
juniper_inside = "set security nat static rule-set %s rule %s match destination-address %s\n"
juniper_outside = "set security nat static rule-set %s rule %s then static-nat prefix %s\n"


f = open(output_file_name,"a")
f.write("--------------------------------------------------------------------------------\n")
cli_command = juniper_public_nat % (static_nat_rule_set_name)
f.write(cli_command)
f.close()


for content_in_file in contents_in_file:
   
   [ _public_nat_ip_, _inside_nated_ip_ ] = content_in_file.strip().split("\t")

   f = open(output_file_name,"a")
   f.write("--------------------------------------------------------------------------------\n")

   # rule_name
   public_ip_number = _public_nat_ip_.strip().split(".")
   policy_rule_name = "_".join(public_ip_number)

   # inside
   cli_command = juniper_inside % (static_nat_rule_set_name,policy_rule_name,_public_nat_ip_+"/32") 
   f.write(cli_command)

   # outside
   cli_command = juniper_outside % (static_nat_rule_set_name,policy_rule_name,_inside_nated_ip_+"/32")
   f.write(cli_command)
    
   f.close()
