#! /usr/bin/env python


from Routing_information import Routing_information
from Utility_function import Utility_function
from utils import *
import ipcalc


input_file_names = ["./source.renew","./destination.renew","./global_nat_source.renew","./global_nat_address.renew"]
default_gateway_zone_name = ""


for input_file_name in input_file_names:

   f = open(input_file_name,"r")
   input_file_contents = f.readlines()
   f.close()

   output_file_name = input_file_name.split("renew")[0] + "match_zone"
   f = open(output_file_name,"w")
   f.close()

   for input_file_content in input_file_contents:
    
      f = open(output_file_name,"a") 
      [ policy_sequence, policy_object ] =  input_file_content.strip().split("\t")
      [ policy_object_ip, policy_object_subnet ] = policy_object.split("/")

      match_status_of = False
      # host object is 0.0.0.0/0 means ANY ip address.
      if policy_object == "0.0.0.0/0":
        for _zone_name_ in Routing_information.zone_name:
           msg_string = "\t".join([ policy_sequence, _zone_name_, policy_object ])+"\n"
           f.write(msg_string)
        continue   
  
      #
      matched_subnet_size = 0
      matched_zone_name = ""
      for _zone_name_ in Routing_information.zone_name:
         for _route_network_ in Routing_information.network_mask[_zone_name_]:
            if _route_network_ == "0.0.0.0/0":
              default_gateway_zone_name = _zone_name_
              continue
            #
            [ cidr, subnet ] = _route_network_.strip().split("/")
            if int(policy_object_subnet) < int(subnet):
              continue          
   
            #
            if policy_object in ipcalc.Network(_route_network_):
              if int(matched_subnet_size) < int(subnet):
                matched_subnet_size = int(subnet)
                matched_zone_name = _zone_name_
                match_status_of = True
              continue
      if matched_zone_name:
        msg_string = "\t".join([ policy_sequence, matched_zone_name, policy_object ])+"\n" 
        f.write(msg_string)

      #
      for _zone_name_ in Routing_information.zone_name:
         for _route_network_ in Routing_information.network_mask[_zone_name_]:
            if _route_network_ == "0.0.0.0/0":
              default_gateway_zone_name = _zone_name_
              continue
            #
            [ cidr, subnet ] = _route_network_.strip().split("/")
            if int(policy_object_subnet) < int(subnet):
              if cidr in ipcalc.Network(policy_object):   
                msg_string = "\t".join([ policy_sequence, _zone_name_, _route_network_ ])+"\n"
                match_status_of = True
                f.write(msg_string)
      #
      if not match_status_of:
        msg_string = "\t".join([ policy_sequence, default_gateway_zone_name, policy_object ])+"\n"
        f.write(msg_string)

      f.close()


