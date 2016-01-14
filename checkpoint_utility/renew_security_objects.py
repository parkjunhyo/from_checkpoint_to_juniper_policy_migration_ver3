#! /usr/bin/env python

import os, random, time
from ipaddr import IPAddress as ip_address

origin_src_data = "./source.gen"
origin_dst_data = "./destination.gen"
origin_port_data = "./service.gen"

output_src_data = "./source.renew"
output_dst_data = "./destination.renew"
output_port_data = "./service.renew"


# origin_data_list = [origin_src_data, origin_dst_data, origin_port_data]
origin_data_list = [origin_src_data]
output_data_list = [output_src_data, output_dst_data, output_port_data]

random.seed(time.clock())


def lookup_object(policy_no_in, policy_object_in):
   object_name = policy_object_in.rstrip()
   random_name = str(random.random())
   bash_result = random_name.split(".")[1]
   bash_command = "./searching_network_objects.sh %s %s" % (object_name, bash_result)
   os.system(bash_command)
   f = open(bash_result,"r")
   file_contents = f.readlines()
   f.close()
   os.system("rm -rf %s" % (bash_result))

   for file_content in file_contents:
      all_info_list = file_content.split("\t")
      matched_name = all_info_list[0]
      matched_type = all_info_list[1]
      matched_ip = all_info_list[2]
      matched_mask = all_info_list[3]
      matched_installed = all_info_list[4]
      matched_nat = all_info_list[5]
      matched_member = all_info_list[6]
      matched_version = all_info_list[7]
      matched_comments = all_info_list[8]

      if matched_name == object_name and matched_type == "Host Node":
        print "\t".join([policy_no_in, matched_ip+"/32"])

      if matched_name == object_name and matched_type == "Group":
        lookup_object(policy_no_in, matched_member) 

      if matched_name == object_name and matched_type == "Network":
        random_no = str(random.random())
        r_file = random_no.split(".")[1]
        os.system("./ip_calc.sh %s %s %s" % (matched_ip, matched_mask, r_file))
        f = open(r_file,"r")
        renew_matched_info = f.readlines()
        f.close()
        os.system("rm -rf ./%s" % (r_file))
        print "\t".join([policy_no_in,renew_matched_info[0].rstrip()])

      if matched_name == object_name and matched_type == "Address Range":
        first_ip = ip_address(str(matched_ip.split()[0]))
        last_ip = ip_address(str(matched_ip.split()[2]))
        range_ip_list = []
        while first_ip <= last_ip:
           range_ip_list.append(str(first_ip))
           print object_name
           print "\t".join([policy_no_in, str(first_ip)])
           first_ip = first_ip + 1


list_index = 0
for origin_data in origin_data_list:

   f = open(origin_data,"r")
   read_contents = f.readlines()
   f.close()

   for read_content in read_contents:

      read_content_list = read_content.split("\t")

      policy_no = read_content_list[0]
      policy_object = read_content_list[1]


      lookup_object(policy_no,policy_object)

      
