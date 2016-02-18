#! /usr/bin/env python

import sys
from Routing_information import Routing_information

read_file_name = "./text_type_result.txt"
output_file_name = "./juniper_policy_command.txt"

f = open(read_file_name,"r")
contents = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()


juniper_source_command = "set security policies from-zone %s to-zone %s policy %s match source-address %s"
juniper_destination_command = "set security policies from-zone %s to-zone %s policy %s match destination-address %s"
juniper_application_command = "set security policies from-zone %s to-zone %s policy %s match application %s"
juniper_permit_command = "set security policies from-zone %s to-zone %s policy %s then permit"
juniper_log_command = "set security policies from-zone %s to-zone %s policy %s then log session-close"

for content_in in contents:

   content_list = content_in.split("\t")
   policy_no = content_list[0]
   policy_status = content_list[1]
   policy_from = content_list[2]
   policy_source_address = content_list[3].split(";")
   policy_to = content_list[4]
   policy_destination_address = content_list[5].split(";")
   policy_service = content_list[6].strip().split(";")
   policy_rule_name = "%s_%s%s" % (policy_no,policy_from,policy_to)

   f = open(output_file_name,"a")

   for _source_address_ in policy_source_address:
      in_msg = juniper_source_command % (policy_from,policy_to,policy_rule_name,_source_address_)
      f.write(in_msg+"\n")

   for _destination_address_ in policy_destination_address:
      in_msg = juniper_destination_command % (policy_from,policy_to,policy_rule_name,_destination_address_)
      f.write(in_msg+"\n")

   for _service_ in policy_service:
      service_object = "_".join(_service_.upper().split(":"))
      in_msg = juniper_application_command % (policy_from,policy_to,policy_rule_name,service_object)
      f.write(in_msg+"\n")

   in_msg = juniper_permit_command % (policy_from,policy_to,policy_rule_name)
   f.write(in_msg+"\n")

   in_msg = juniper_log_command % (policy_from,policy_to,policy_rule_name)
   f.write(in_msg+"\n")

   f.close()
