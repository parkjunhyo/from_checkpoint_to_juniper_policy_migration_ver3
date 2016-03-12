#! /usr/bin/env python

import sys
from Routing_information import Routing_information

files_name_list_to_read = {
                            "source":"./source.match_zone", 
                            "destination":"./destination.match_zone", 
                            "service":"./service.renew",
                            "comment":"./comment.renew"
                          }

outfile_name = "./juniper_type_result.txt"
text_type_outfile_name = "./text_type_result.txt"

def readFile(file_name):
   f = open(file_name, "r")
   contents = f.readlines()
   f.close()
   return contents


def checkData_validation(data_list_type):
   index_list = []
   for content in data_list_type:
      policy_number = content.rstrip().split("\t")[0]
      if int(policy_number) not in index_list:
        index_list.append(int(policy_number))
   if len(index_list) != max(index_list):
     not_valid = []
     for i_ in range(len(index_list)):
        number_ = i_ + 1
        if (number_ not in index_list) and (number_ not in not_valid):
          not_valid.append(number_)
     print "%s is not matched" % (str(not_valid))
     sys.exit(0)
   return max(index_list), len(index_list)


def sorting_by_policy_number(max_policy_number, data_list_type):
   sorting_list = [] 
   for i_ in range(max_policy_number):
      members_list = []
      policy_number = i_ + 1
      for content in data_list_type:
         _policy_number_ = content.rstrip().split("\t")[0]
         _members_ = content.rstrip().split("\t")[1:]
         if policy_number == int(_policy_number_):
           if _members_ not in members_list:
             members_list.append(_members_)
      if [ policy_number, members_list ] not in sorting_list:
        sorting_list.append([ policy_number, members_list ])
   return sorting_list 

def sorting_by_zone_name(data_list_type):
   sorting_list = []
   for content in data_list_type:
      policy_number = content[0]
      zone_object_combination_list = []      
      for zone_name_ in Routing_information.zone_name:
         object_group = []
         for objects_list in content[1]:
            _zone_name_ = objects_list[0]
            _object_ = objects_list[1]
            if zone_name_ == _zone_name_:
              if _object_ not in object_group:
                object_group.append(_object_)
         # not matched zone
         if len(object_group) != 0:
           if [ zone_name_, object_group ] not in zone_object_combination_list:
             zone_object_combination_list.append([ zone_name_, object_group ])
      # by policy number
      if [ policy_number, zone_object_combination_list ] not in sorting_list:
        sorting_list.append([ policy_number, zone_object_combination_list ])
   return sorting_list
            
def searching_object_matched_ruld_number(policy_rule_number, data_list_type):
   for content in data_list_type:
      _policy_number_ = content[0]
      if policy_rule_number == _policy_number_:
        return content[1]

source_contents = readFile(files_name_list_to_read["source"])
destination_contents = readFile(files_name_list_to_read["destination"])
service_contents = readFile(files_name_list_to_read["service"])

src_max, src_len = checkData_validation(source_contents)
dst_max, dst_len = checkData_validation(destination_contents)
srv_max, srv_len = checkData_validation(service_contents)

if src_max != dst_max or src_max != srv_max or dst_max != srv_max:
  print "source max : %s, destination max : %s, service max : %s are not matched" % (str(src_max), str(dst_max), str(srv_max))
  sys.exit(0)


sorted_source = sorting_by_policy_number(src_max, source_contents)
sorted_destination = sorting_by_policy_number(dst_max, destination_contents)
sorted_service = sorting_by_policy_number(srv_max,service_contents)

if len(sorted_source) != len(sorted_destination) or len(sorted_source) != len(sorted_service) or len(sorted_destination) != len(sorted_service):
  print "sourted source : %s, sourted destination : %s, sourted service : %s are not matched" % (str(len(sorted_source)), str(len(sorted_destination)), str(len(sorted_service)))
  sys.exit(0)

sorted_by_zone_source = sorting_by_zone_name(sorted_source)
sorted_by_zone_destination = sorting_by_zone_name(sorted_destination)

if len(sorted_by_zone_source) != len(sorted_by_zone_destination) or len(sorted_by_zone_source) != len(sorted_service) or len(sorted_by_zone_destination) != len(sorted_service):
  print "sourted source : %s, sourted destination : %s, sourted service : %s are not matched" % (str(len(sorted_by_zone_source)), str(len(sorted_by_zone_destination)), str(len(sorted_service)))
  sys.exit(0)

# comment read
f = open(files_name_list_to_read["comment"],"r")
comment_contents = f.readlines()
f.close()

_idx_list_ = []
_cmt_list_ = []
for comment_content in comment_contents:
   [ _index_no_, _comment_ ] = comment_content.strip().split("\t")
   re_string_ = _comment_.split("\xc2\xa0")[0]
   _idx_list_.append(str(_index_no_))
   _cmt_list_.append(str(re_string_))

comment_dict = dict(zip(_idx_list_,_cmt_list_))

# print out
policy_rule_number = len(sorted_by_zone_source)
policy_index = 0
f = open(outfile_name,"w")
f.close()
p = open(text_type_outfile_name,"w")
p.close()
for i_ in range(policy_rule_number):
   policy_index = i_ + 1
   # source destination combination
   f = open(outfile_name,"a")
   p = open(text_type_outfile_name,"a")
   f.write("\n")
   f.write("-------------------------------------------- Policy : %s --------------------------------------\n" % (str(policy_index)))
   for _source_value_ in searching_object_matched_ruld_number(policy_index, sorted_by_zone_source):
      for _destination_value_ in searching_object_matched_ruld_number(policy_index, sorted_by_zone_destination):

         rule_status = ""
         if _source_value_[0] == _destination_value_[0]:
           rule_status = "NOT_OK"  
         else:
           rule_status = "OK"

         f.write("\n\n")
         f.write("Policy ID : %s, From : %s, To : %s  ..... [ %s ] [ %s_%s%s ]\n\n" % (str(policy_index),_source_value_[0],_destination_value_[0],rule_status,str(policy_index),_source_value_[0],_destination_value_[0]))
         f.write("Source IP Address : \n")
         source_members_string = ""
         source_members_group = []
         for _src_network_ in _source_value_[1]:
            source_members_group.append(_src_network_)
            f.write(_src_network_+"\n")
         source_members_string = ";".join(source_members_group)
         ##f.write("\n")

         f.write("Destination IP Address : \n")
         desti_members_string = ""
         desti_members_group = []
         for _dst_network_ in _destination_value_[1]:       
            desti_members_group.append(_dst_network_)
            f.write(_dst_network_+"\n")
         desti_members_string = ";".join(desti_members_group) 
         # service combination
         f.write("\n")

         f.write("Service Port: \n")
         port_members_string = ""
         port_members_group = []
         for _service_value_ in searching_object_matched_ruld_number(policy_index, sorted_service):
            port_members_group.append(":".join(_service_value_))
            if len(_service_value_) == 1:
              service_msg = " Port Number : %s" % (_service_value_[0])
            else:
              service_msg = " Proto type : %s, Port Number : %s" % (_service_value_[0],_service_value_[1])
            f.write(service_msg+"\n")
         port_members_string = ";".join(port_members_group)

         # comment
         f.write("\n")
         f.write("Comment: \n")
         f.write(str(comment_dict[str(policy_index)].strip()))      
         f.write("\n")


         all_member_string = "\t".join([str(policy_index), rule_status, _source_value_[0], source_members_string, _destination_value_[0], desti_members_string, port_members_string, str(comment_dict[str(policy_index)])])
         p.write(all_member_string+"\n")


   p.close()
   f.close()
 

