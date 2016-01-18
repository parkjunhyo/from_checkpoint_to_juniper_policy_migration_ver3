#! /usr/bin/env python


from Routing_information import Routing_information
from Utility_function import Utility_function
from utils import *
import ipcalc

class Match_zone_from_network:
 
  default_zone_name = "" 
  read_files_name = ["./source.renew","./destination.renew"]
  output_files_name = ["./source.match_zone","./destination.match_zone"]
  database_network_zone = {}

  def writeOutput(self, file_name, input_data):
     string_msg = "\t".join(input_data)+"\n"
     f = open(file_name,"a")
     f.write(string_msg)
     f.close()

  def Start(self):

     # find default gateway zone name
     self.default_zone_name = findDefaultzone(Routing_information.zone_name, Routing_information.network_mask)

     # read file 
     file_index = 0
     for read_file_name in self.read_files_name:
        f = open(read_file_name,"r")
        contents_in_read_file = f.readlines()
        f.close()

        # output file initailzation
        out_file_name = self.output_files_name[file_index]
        f = open(out_file_name,"w")
        f.close()
 
        for content_in_read_file in contents_in_read_file:
           [ policy_number, policy_object ] = content_in_read_file.rstrip().split("\t")  
           [ ip_address, subnet_size ] = policy_object.split("/")
        
           # searching database and fine zone according to network
           if policy_object not in self.database_network_zone.keys():

             # default zone
             if "0.0.0.0/0" == policy_object:
               self.database_network_zone[policy_object] = self.default_zone_name
               combination = [ policy_number, self.default_zone_name, policy_object ]
               self.writeOutput(out_file_name, combination)
               continue

             # find zone name.. ratating all routing information
             compare_subnet_size = "0"
             match_status = False
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
                   else:
                     if _ip_address_ in ipcalc.Network(policy_object):
                       combination = [ policy_number, _zone_name_, _network_mask_ ]
                       self.writeOutput(out_file_name, combination)
            
             # Not matched case, it will be default gateway zone. 
             if not match_status:
               self.database_network_zone[policy_object] = self.default_zone_name
               combination = [ policy_number, self.default_zone_name, policy_object ]
               self.writeOutput(out_file_name, combination)
             else:
               combination = [ policy_number, self.database_network_zone[policy_object], policy_object ]
               self.writeOutput(out_file_name, combination)

           # searching database and fine zone according to network
           else:
             combination = [ policy_number, self.database_network_zone[policy_object], policy_object ]
             self.writeOutput(out_file_name, combination)

        # go to next file
        print read_file_name + " has been done!"
        file_index = file_index + 1


if __name__=="__main__":
  root_process = Match_zone_from_network()
  root_process.Start()
