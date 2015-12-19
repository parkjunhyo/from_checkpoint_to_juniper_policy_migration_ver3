#! /usr/bin/env python

from Routing_information import Routing_information
from Utility_function import Utility_function

import sys, time
from netaddr import *


class Compare_fw_policies(Routing_information,Utility_function):

  default_zone_name = ""
  _subnet_size = [8, 16, 24]
  zone_candidate_network = []
  policy_sequence_count = 0

  def Insert_zone_category( self, string_ruleid_and_object_list ): 

   return_result_list = []

   # start for
   total_number = len(string_ruleid_and_object_list)
   thread_count = 1
   for string_ruleid_and_object in string_ruleid_and_object_list:
      start_time = time.time() 
      string_ruleid_and_object_without_blank = string_ruleid_and_object.strip()
      [ ruleid, object_value ] = string_ruleid_and_object_without_blank.split()
      [ ip_value, mask_value ] = object_value.split("/")
      input_network = object_value
      input_ip_value = ip_value
      input_mask_value = mask_value

      # input status check
      if input_network == "0.0.0.0/0":
        return_result_list.append([ruleid, self.default_zone_name, input_network])
        end_time = time.time()
        print "[%s/%s] done, process time : %s" % (str(thread_count),str(total_number),str(int(end_time)-int(start_time)))
        thread_count = thread_count + 1
        continue

      # Longest match , Big network calcuration 
      matched_net_info = []
      for candi_netmask in self.zone_candidate_network:
         [ candi_ip_addr, candi_mask ] = candi_netmask.split("/")
         comparing_network = candi_netmask
         comparing_ip_value = candi_ip_addr
         comparing_mask_value = candi_mask
         for zone_n in self.zone_name:
            if comparing_network in self.network_mask[ zone_n ]:
                current_zone_name = zone_n
                break

         ## input = small net(mask is big), comparing = big(mask is small)
         if int(input_mask_value) > int(comparing_mask_value):
           div_value_list = []
           status = False
           for sub_value in self._subnet_size:
              if int(comparing_mask_value) <= sub_value and sub_value <= int(input_mask_value):
                div_value_list.append(sub_value)
                status = True
           if not status: 
                div_value_list = [ int(input_mask_value) ]

           # input network change 
           origin_data_list = input_ip_value.split(".")
           update_data_list = ["0","0","0","0"]
           value, last = divmod(max(div_value_list),8)
           if last == 0:
             for i in range(value):
                update_data_list[i] = str(origin_data_list[i])
             new_ip_value = ".".join(update_data_list) + "/" + str(value*8)   
           else:
             new_ip_value = input_network         
             
           div_value = max(div_value_list)           
           standard_value = int(new_ip_value.split("/")[1])

           print "div_value : %s, standard_value : %s" % (str(div_value),str(standard_value))

           comparing_net_module = IPNetwork(comparing_network) 
           first_division_module = list(comparing_net_module.subnet(standard_value))
           input_net_module = IPNetwork(new_ip_value)
           if input_net_module in first_division_module:
             # matched_net_info.append([current_zone_name, comparing_network])
             matched_net_info.append([current_zone_name, input_network])
         ## input = small net(mask is big), comparing = big(mask is small)
         ## end of "if int(input_mask_value) > int(comparing_mask_value):"

      # end of "for candi_netmask in self.zone_candidate_network:"
      if len(matched_net_info) == 0:
        return_result_list.append([ruleid, self.default_zone_name, input_network])
      else:
        # extract : matched_net_info.append([current_zone_name, comparing_network])
        temp_mask_only = []
        for s_ in matched_net_info:
           temp_mask_only.append(int(s_[1].split("/")[1]))
        max_mask = max(temp_mask_only)
        for s_ in matched_net_info:
           if max_mask == int(s_[1].split("/")[1]):
             return_result_list.append([ruleid, s_[0], s_[1]])
             break

      # Longest match , same network calcuration 
      matched_net_info = []
      for candi_netmask in self.zone_candidate_network:
         [ candi_ip_addr, candi_mask ] = candi_netmask.split("/")
         comparing_network = candi_netmask
         comparing_ip_value = candi_ip_addr
         comparing_mask_value = candi_mask
         for zone_n in self.zone_name:
            if comparing_network in self.network_mask[ zone_n ]:
                current_zone_name = zone_n
                break

         ## input = comparing : same subnet
         if int(input_mask_value) == int(comparing_mask_value):
           if input_network == comparing_network:
             change_status = None
             index_number = 0
             ## find out target
             for values_list in return_result_list:
                _x_rule_id = values_list[0]
                _x_zone_name = values_list[1]
                _x_network = values_list[2]
                if comparing_network == _x_network:
                  change_status = index_number
                  break
                else:
                  index_number = index_number + 1
             ## find out target
             if change_status == None:
               return_result_list.append([_x_rule_id, current_zone_name, comparing_network]) 
             else:
               return_result_list[index_number] = [_x_rule_id, current_zone_name, comparing_network]
      # end of "for candi_netmask in self.zone_candidate_network:" 

      # Longest match , small network calcuration 
      matched_net_info = []
      for candi_netmask in self.zone_candidate_network:
         [ candi_ip_addr, candi_mask ] = candi_netmask.split("/")
         comparing_network = candi_netmask
         comparing_ip_value = candi_ip_addr
         comparing_mask_value = candi_mask
         for zone_n in self.zone_name:
            if comparing_network in self.network_mask[ zone_n ]:
                current_zone_name = zone_n
                break

         ## input = big net(mask is small), comparing = small(mask is big)
         if int(input_mask_value) < int(comparing_mask_value):
           input_net_module = IPNetwork(input_network)
           first_division_module = list(input_net_module.subnet(int(comparing_mask_value)))
           comparing_net_module = IPNetwork(comparing_network)
           if comparing_net_module in first_division_module:
             return_result_list.append([ruleid, current_zone_name, comparing_network])
      # end of "for candi_netmask in self.zone_candidate_network:"
      end_time = time.time()
      print return_result_list
      print "[%s/%s] done, process time : %s" % (str(thread_count),str(total_number),str(int(end_time)-int(start_time)))
      thread_count = thread_count + 1
   # end of "for string_ruleid_and_object in string_ruleid_and_object_list:"
   return return_result_list # def Insert_zone_category( self, string_ruleid_and_object_list ):


  def _varidation_check( self, value_in_list ):


     print value_in_list

     return_true_or_not = True
     # find sequence list 
     sequence_list = []
     for value_ in value_in_list:
        seqid = value_[0]
        if str(seqid) not in sequence_list:
          sequence_list.append(str(seqid))
     
     max_seqid = sequence_list[-1]
     self.policy_sequence_count = max_seqid

     real_index = 0
     for index in range(int(max_seqid)):
        real_index = index + 1
        if str(real_index) not in sequence_list:
          print "[ error ] input data is not matched : \"" + str(real_index) + "\""
          return_true_or_not = False
          sys.exit(0)
     # return
     return return_true_or_not   # def _varidation_check( self, list_item ):



  def Sequence_object_group_arrange( self, value_in_list ):

     if self._varidation_check( value_in_list ):
       return_result_seq_zone_net_comb = [] 
       # sorting
       for index in range(int(self.policy_sequence_count)):
          real_index = index + 1
          # find target with index number only
          candi_list = []
          for value_ in value_in_list:
             seqid = value_[0]
             if str(seqid) == str(real_index):
               if value_ not in candi_list:
                 candi_list.append(value_)
          # candidate list for zone name
          zone_name_group = []
          for value_ in candi_list:
             zn = value_[1]
             if zn not in zone_name_group:
               zone_name_group.append(zn)

          # zn_sum = [[zone_name, [ matched_network ]],[zone_name, [ matched_network ]]] 
          zn_sum = []
          for value_ in zone_name_group:
             zn = value_
             zn_comb = []
             for value_b in candi_list:
                if zn == value_b[1]:
                  if value_b[2] not in zn_comb:
                    zn_comb.append(value_b[2])
             if [zn, zn_comb] not in zn_sum:
               zn_sum.append([zn, zn_comb])      

          # zn_sum = [[zone_name, [ matched_network ]],[zone_name, [ matched_network ]]] 
          if [real_index, zn_sum] not in return_result_seq_zone_net_comb:
            return_result_seq_zone_net_comb.append([real_index, zn_sum])
       # sorting
       return return_result_seq_zone_net_comb

  def Start( self ):

   for zone_n in self.zone_name:
     if "0.0.0.0/0" in self.network_mask[zone_n]:
      self.default_zone_name = zone_n
     else:
      continue


   for value_in_list in self.network_mask.values():
     for value_in_tuple in value_in_list:
        if value_in_tuple == "0.0.0.0/0":
            continue
        if value_in_tuple not in self.zone_candidate_network:
            self.zone_candidate_network.append( value_in_tuple )

   # source 
   string_ruleid_and_object_list = self.Read_file("./source_ip_address.txt")
   source_ruleid_zone_ipnet = self.Insert_zone_category( string_ruleid_and_object_list )
   final_source_list = self.Sequence_object_group_arrange( source_ruleid_zone_ipnet )
   print "source data has been processed.."

   # destination
   string_ruleid_and_object_list = self.Read_file("./destination_ip_address.txt")
   destination_ruleid_zone_ipnet = self.Insert_zone_category( string_ruleid_and_object_list )
   final_destination_list = self.Sequence_object_group_arrange( destination_ruleid_zone_ipnet )
   print "destination data has been processed.."

   # service
   service_ruleid_port = []
   string_ruleid_and_object_list = self.Read_file("./service.txt")
   for string_v in string_ruleid_and_object_list:
      string_v_without_blank = string_v.strip()
      [ ruleid_, service_ ] = string_v_without_blank.split()
      service_ruleid_port.append([ ruleid_, service_ ])
   final_service_list = []
   for index in range(int(self.policy_sequence_count)):
      real_index = index + 1
      matched_list = []
      for index_i in service_ruleid_port:
         if int(real_index) == int(index_i[0]):
           if str(index_i[1]) not in matched_list:
             matched_list.append(str(index_i[1]))
      if [real_index, matched_list] not in final_service_list:
        final_service_list.append([real_index, matched_list])
   # service
   print "service data has been processed..!"
   # print out
   file_f = open("./juniper_type_policy_result.txt", "w")
   file_s = open("./string_type_policy_result.txt", "w")
   for index in range(int(self.policy_sequence_count)):
      real_index = index + 1
      # source
      matched_src = []
      for fl_ in final_source_list:
         if int(fl_[0]) == int(real_index):
           matched_src = fl_[1]
           break
      # destination
      matched_dst  = []
      for fl_ in final_destination_list:
         if int(fl_[0]) == int(real_index):
           matched_dst = fl_[1]
           break
      # service
      matched_srv  = []
      for fl_ in final_service_list:
         if int(fl_[0]) == int(real_index):
           matched_srv  = fl_[1]
           break
      # print out
      for ms_ in matched_src:
         from_zone = ms_[0]
         from_net = ms_[1]
         for md_ in matched_dst:
            to_zone = md_[0]
            to_net = md_[1]
            
            status = "Good"
            if str(from_zone) == str(to_zone):
              status = "Not Good, Not Valid"
            
            file_f.write("\n")
            file_f.write("Rule No [ %s ] : from \"%s\" to \"%s\", Status [ %s ] \n\n" % (str(real_index), from_zone, to_zone, status))
            file_f.write("Source Network : \n")
            for fn_ in from_net:
               file_f.write(str(fn_)+"\n")
            file_f.write("\n")
            file_f.write("Destination Network : \n")
            for fn_ in to_net:
               file_f.write(str(fn_)+"\n")
            file_f.write("\n")
            # service print out
            file_f.write("Service, Application : \n")
            for ms_ in matched_srv:
               file_f.write(str(ms_)+"\n")

            # string type print out
            string_from_net = ";".join(from_net)
            string_to_net = ";".join(to_net)
            string_service = ";".join(matched_srv)
            string_all_msg = "%s\t %s\t %s\t %s\t %s\t %s\t %s\n" % (str(real_index), status, from_zone, string_from_net, to_zone, string_to_net, string_service)
            file_s.write(string_all_msg)
      file_f.write("\n")
      file_f.write("---------------------------------------------------------\n")
   # print out
   file_f.close()
   file_s.close()


if __name__=="__main__":
 root_process= Compare_fw_policies()
 root_process.Start()
