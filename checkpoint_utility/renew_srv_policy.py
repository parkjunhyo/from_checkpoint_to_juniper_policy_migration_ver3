#! /usr/bin/env python

import os, random, time
from ipaddr import IPAddress as ip_address

origin_port_data = "./service.gen"

output_port_data = "./service.renew"


origin_data_list = [origin_port_data]
output_data_list = [output_port_data]

random.seed(time.clock())


def lookup_object(policy_no_in, policy_object_in, output_file_name):


   if policy_object_in == "Any\n":
     f = open(output_file_name,"a")
     f.write("\t".join([policy_no_in, "Any\n"]))
     f.close()
     return

   object_name = policy_object_in.rstrip()
   random_name = str(random.random())
   bash_result = random_name.split(".")[1]
   bash_command = "./searching_service_objects.sh %s %s" % (object_name, bash_result)
   os.system(bash_command)
   f = open(bash_result,"r")
   file_contents = f.readlines()
   f.close()
   os.system("rm -rf %s" % (bash_result))


   for file_content in file_contents:
      all_info_list = file_content.split("\t")
      matched_name = all_info_list[0]
      matched_type = all_info_list[1]
      matched_port = all_info_list[2]
      matched_prototype = all_info_list[3]
      matched_matchany = all_info_list[4]
      matched_sourceport = all_info_list[5]
      matched_members = all_info_list[6]
      matched_comments = all_info_list[7]

  
      match_status = False
      if matched_name == object_name and (matched_type == "TCP" or matched_type == "Tcp" or matched_type == "tcp" or matched_type == "UDP" or matched_type == "Udp" or matched_type == "udp" or matched_type == "OTHER" or matched_type == "Other" or matched_type == "other" or matched_type == "RPC" or matched_type == "Rpc" or matched_type == "rpc"):
        f = open(output_file_name,"a")
        f.write("\t".join([policy_no_in, matched_type, matched_port+"\n"]))
        f.close()
        match_status =  True

      if matched_name == object_name and (matched_type == "GROUP" or matched_type == "Group" or matched_type == "group"):
        lookup_object(policy_no_in, matched_members, output_file_name) 
        match_status =  True

      if not match_status and matched_name == object_name:
        f = open(output_file_name,"a")
        f.write("\t".join([policy_no_in, matched_type, matched_name+"\n"]))
        f.close()
        match_status =  True

   

list_index = 0
for origin_data in origin_data_list:

   f = open(origin_data,"r")
   read_contents = f.readlines()
   f.close()

   output_file_name = output_data_list[list_index]
   f = open(output_file_name,"w")
   f.close()
   for read_content in read_contents:
      read_content_list = read_content.split("\t")
      policy_no = read_content_list[0]
      policy_object = read_content_list[1]
      lookup_object(policy_no,policy_object,output_file_name)
      print "policy number [ %s ] has been done" % (policy_no)

   list_index = list_index + 1

      
