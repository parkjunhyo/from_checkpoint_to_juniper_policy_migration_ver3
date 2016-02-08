#! /usr/bin/env python

import sys
from Routing_information import Routing_information
import ipcalc


source_data_to_read = "./checkpoint_utility/network_objects.gen"
output_file_name = "./static_nat_address.txt"


f = open(source_data_to_read,"r")
contents = f.readlines()
f.close()

f = open(output_file_name,"w")
f.close()

for content in contents:
   
   elements = content.split("\t")
   element_name = elements[0]
   element_type = elements[1]
   element_ip = elements[2]
   element_netmask = elements[3]
   element_products_installed = elements[4]
   element_nat_address = elements[5]
   element_member = elements[6]
   element_version = elements[7]
   element_comment = elements[8]

   if element_nat_address != "-":
     for public_network in Routing_information.public_nat_network:
        try:
          if element_nat_address in ipcalc.Network(public_network):
            msg_to_write = "\t".join([element_nat_address, element_ip])+"\n"
            f = open(output_file_name,"a")
            f.write(msg_to_write)
            f.close()
        except:
          continue
        



