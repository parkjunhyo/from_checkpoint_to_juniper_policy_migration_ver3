#! /usr/bin/env python


from Routing_information import Routing_information
from Utility_function import Utility_function
from utils import *
import ipcalc

class Policy_source_ip_address_renew:
 
  default_zone_name = "" 
  read_files_name = ["./source.renew"]
  database_network_zone = {}

  def Start(self):

     # find default gateway zone name
     self.default_zone_name = findDefaultzone(Routing_information.zone_name, Routing_information.network_mask)

     # read file 
     for read_file_name in self.read_files_name:
        f = open(read_file_name,"r")
        contents_in_read_file = f.readlines()
        f.close()
 
        for content_in_read_file in contents_in_read_file:
           [ policy_number, policy_object ] = content_in_read_file.rstrip().split("\t")  
           [ ip_address, subnet_size ] = policy_object.split("/")
        
           # searching database and fine zone according to network
           if policy_object not in self.database_network_zone.keys():

             # default zone
             if "0.0.0.0/0" == policy_object:
               self.database_network_zone[policy_object] = self.default_zone_name
               print [policy_number, self.default_zone_name, policy_object+"\n"]
               continue
             # find zone name.. ratating all routing information
             
             compare_subnet_size = "0"
             match_status = False
             match_zone_name = ""
             for _zone_name_ in Routing_information.zone_name:
                for _network_mask_ in Routing_information.network_mask[_zone_name_]:

                   if "0.0.0.0/0" == _network_mask_:
                     continue
                   # target information
                   [ _ip_address_, _subnet_size_ ] = _network_mask_.rstrip().split("/")

                   if int(subnet_size) >= int(_subnet_size_):
                     if ip_address in ipcalc.Network(_network_mask_):
                       if int(compare_subnet_size) < int(_subnet_size_):
                         compare_subnet_size = _subnet_size_
                         self.database_network_zone[policy_object] = _zone_name_
                         match_status = True
                         match_zone_name = _zone_name_ 
            
             # Not matched case, it will be default gateway zone. 
             if not match_status:
               self.database_network_zone[policy_object] = self.default_zone_name
               print [policy_number, self.default_zone_name, policy_object+"\n"]
             else:
               print [policy_number, self.database_network_zone[policy_object], policy_object+"\n"]

           # searching database and fine zone according to network
           else:
             print ["D", policy_number, self.database_network_zone[policy_object], policy_object+"\n"]


if __name__=="__main__":
  root_process = Policy_source_ip_address_renew()
  root_process.Start()
