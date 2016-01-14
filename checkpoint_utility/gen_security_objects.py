#! /usr/bin/env python

### file names descriptions
origin_src_data = "./Data/source.data"
origin_dst_data = "./Data/destination.data"
origin_port_data = "./Data/service.data"

output_src_data = "./source.gen"
output_dst_data = "./destination.gen"
output_port_data = "./service.gen"

policy_no_limit = range(100000)
policy_no_str_list = map(str,policy_no_limit)
policy_no_str_list.append("-")

origin_data_list = [origin_src_data, origin_dst_data, origin_port_data]
output_data_list = [output_src_data, output_dst_data, output_port_data]

list_index = 0
above_no = ""
above_object = ""


for origin_data in origin_data_list:

   f = open(origin_data,"r")
   read_contents = f.readlines()
   f.close()


   f = open(output_data_list[list_index],"w")
   for read_content in read_contents:

      read_content_list = read_content.split("\t")   

      policy_no = read_content_list[0]
      policy_object = read_content_list[1]

      if policy_no not in policy_no_str_list:
        continue


      if policy_no == "-" and policy_object == "-\n":
        continue

      if policy_no != "-" and policy_object != "-\n":
        above_no = policy_no
        above_object = policy_object
        # write the result
        line_to_write = "\t".join(read_content_list)
        f.write(line_to_write)
        continue

      if policy_no == "-" and policy_object != "-\n":
        read_content_list[0] = above_no
        # write the result
        line_to_write = "\t".join(read_content_list)
        f.write(line_to_write)
        continue

      if policy_no != "-" and policy_object == "-\n":
        above_no = policy_no
        continue

   f.close()

   # list_index count
   list_index = list_index + 1

