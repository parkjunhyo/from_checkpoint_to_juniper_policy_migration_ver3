#! /usr/bin/env python


import os
import sys
from netaddr import *                        ## for ip in IPSet(['192.0.2.0/28','192.0.2.255/28']):
                                             ##   print str(ip)
from ipaddr import IPAddress as ip_address   ## def findIPs( self, start, end ):


class Sorting_input_data:


 distributed_policies_list_in_list = []

 def File_writelines( self, input_data_list, file_name ):
  file_f = open(file_name, "w")
  for data_list in input_data_list:
     in_msg = "\t".join(data_list) + "\n"
     file_f.write(in_msg)
  file_f.close()

 def File_readlines_output_list( self, file_name ):
   f = open( file_name)
   contents = f.readlines()
   f.close()
   return contents

 def findIPs( self, start, end ):
    start = ip_address(str(start))
    end = ip_address(str(end))
    result = []
    while start <= end:
        result.append(str(start))
        start += 1
    return result



 def Distributed_by_objecttype( self, input_data, object_table ):

   for in_ in input_data:
    # definition
    sequence_id = in_[0]
    object_name = in_[1]

    # find type
    matched_type = ""
    matched_status = 0
    for table_ in object_table:
      if table_[0] == object_name:
        matched_status = matched_status + 1
        matched_type = table_[1]

        if matched_type == "Host Node":
          host_node_ip = table_[2] + "/32"
          self.distributed_policies_list_in_list.append([sequence_id, host_node_ip])
          # result_msg = "%s %s" % (sequence_id, table_[2])
          # print result_msg

        elif matched_type == "Address Range":
          network_range_list = table_[2].split()
          start_ip = network_range_list[0]
          end_ip = network_range_list[-1]
          for single_ip in self.findIPs( start_ip, end_ip ):
             host_node_ip = single_ip + "/32"
             self.distributed_policies_list_in_list.append([sequence_id, host_node_ip])
             # result_msg = "%s %s" % (sequence_id, single_ip)
             # print result_msg

        elif matched_type == "Network":
          net_network = table_[2]
          net_mask = table_[3]
          command = "./ip_calc.sh %s %s" % (net_network, net_mask)
          os.system(command)
          calcurated_network = self.File_readlines_output_list( "./result.ip_calc" )
          os.system("rm -rf ./result.ip_calc")
          # find start ip and end ip
          first_last_list = []
          for string_msg in calcurated_network:
             result_ = string_msg.split()
             try:
                if result_[0] == "Network:":
                     host_node_ip = str(result_[1])
                # if result_[0] == "HostMin:":
                #      first_last_list.append(str(result_[1]))
                # if result_[0] == "HostMax:":
                #      first_last_list.append(str(result_[1]))
             except:
                pass
          # print
          self.distributed_policies_list_in_list.append([sequence_id, host_node_ip])
          # for single_ip in first_last_list:
             # self.distributed_policies_list_in_list.append([sequence_id, single_ip])
             # result_msg = "%s %s" % (sequence_id, single_ip)
             # print result_msg

        elif matched_type == "Group":
          selected_group_list = []
          for selected_object_list in object_table:
            if object_name == selected_object_list[0] and matched_type == selected_object_list[1]:
                  selected_group_list.append([sequence_id, selected_object_list[5]])
          self.Distributed_by_objecttype( selected_group_list, object_table )

        else:      # others
          host_node_ip = ''
          if table_[3] == '-' or table_[3] == '':
            host_node_ip = table_[2] + "/32"            
          else:
            command = "./ip_calc.sh %s %s" % (table_[2], table_[3])
            os.system(command)
            calcurated_network = self.File_readlines_output_list( "./result.ip_calc" )
            os.system("rm -rf ./result.ip_calc")
            for string_msg in calcurated_network:
               result_ = string_msg.split()
               try:
                  if result_[0] == "Network:":
                     host_node_ip = str(result_[1])
               except:
                  print "this is not object which is valid!"
                  os.exit(0)

          self.distributed_policies_list_in_list.append([sequence_id, host_node_ip])
          # result_msg = "%s %s" % (sequence_id, table_[2])
          # print result_msg

        break   # for table_ in object_table:

    if matched_status == 0:
        self.distributed_policies_list_in_list.append([sequence_id, "0.0.0.0/0"])
        # result_msg = "%s %s" % (sequence_id, "0.0.0.0")
        # print result_msg

   return self.distributed_policies_list_in_list   # Distributed_by_objecttype( self, input_data, object_table ):
 
 # [ [ seq, object ], [ seq, object ] ]
 def Raw_datafile_verification( self, file_name ):
   Raw_source_file_contents = self.File_readlines_output_list( file_name )
   Raw_source_file_contents_list = []
   line_number = 1
   # data format confirm
   for content_in_file in Raw_source_file_contents:
      content_without_side_blank = content_in_file.strip()
      content_list = content_without_side_blank.split("\t")
      # the number of data verification
      if len(content_list) != 2:
         print "\" [" + str(line_number) +" ] " + content_without_side_blank + "\" is missed something in " + file_name
         sys.exit(0)
      # first data, integer check
      try:
         except_msg = int(content_list[0])
      except:
         print "\" [" + str(line_number) +" ] " + content_without_side_blank + "\" is missed something in " + file_name
         sys.exit(0)

      # second data confirm
      if content_list[1] != "-" or len(content_list[1]) != 1:
         Raw_source_file_contents_list.append( content_list )
      line_number = line_number + 1

   # data number check
   seq_id_list = []
   for content_in_file in Raw_source_file_contents_list:
      if int(content_in_file[0]) not in seq_id_list:
        seq_id_list.append( int(content_in_file[0]) )
   for number_ in range( seq_id_list[-1] ):
      seq_id_number = number_ + 1
      if seq_id_number not in seq_id_list:
        print "\" " + str( seq_id_number ) +" \" is not existed in " + file_name

   # return
   return Raw_source_file_contents_list   # def Raw_datafile_verification( self, file_name )


 def Output_verification( self, output_list ):
   index_list = []
   for output_ in output_list:
     if int(output_[0]) not in index_list:
          index_list.append(int(output_[0]))

   index_max = index_list[-1]
   for i in range(index_max):
     id_ = i+1
     if id_ not in index_list:
       print "\" " + str(id_) + " \" is missed in output result.!"
       sys.exit(0)

 def Start( self ):

    
   # varidate the data file 
   varidated_source_list = self.Raw_datafile_verification( "./source.gen" )

   # distribute
   data_tobe_write = self.Distributed_by_objecttype( varidated_source_list, object_file_contents_list )

   # output verification
   self.Output_verification( data_tobe_write )

   # print out
   self.File_writelines( data_tobe_write, "./extracted_source_data.txt" )

   print "source processing has been done!"


   # varidate the data file 
   self.distributed_policies_list_in_list = []
   varidated_destination_list = self.Raw_datafile_verification( "./destination.gen" )

   # distribute
   data_tobe_write = self.Distributed_by_objecttype( varidated_destination_list, object_file_contents_list )

   # output verification
   self.Output_verification( data_tobe_write )

   # print out
   self.File_writelines( data_tobe_write, "./extracted_destination_data.txt" )

   print "destination processing has been done!"


   # varidate the data file
   self.distributed_policies_list_in_list = []
   varidated_service_list = self.Raw_datafile_verification( "./service.gen" )

   # output verification
   self.Output_verification( varidated_service_list )

   # print out
   self.File_writelines( varidated_service_list, "./extracted_service_data.txt" )

   print "service processing has been done!"


if __name__=="__main__":
 root_process= Sorting_input_data()
 root_process.Start()
