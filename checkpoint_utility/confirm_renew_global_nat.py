#! /usr/bin/env python

output_src_data = "./global_nat_source.renew"
output_dst_data = "./global_nat_address.renew"

output_data_list = [output_src_data, output_dst_data ]

for output_data in output_data_list:

   f = open(output_data,"r")
   read_contents = f.readlines()
   f.close()

   index_value = []
   for read_content in read_contents:
      contents_list = read_content.split("\t")
      if int(contents_list[0]) not in index_value:
        index_value.append(int(contents_list[0]))

   if len(index_value) != max(index_value):
     print output_data+" is not OK!"
     for i in range(max(index_value)):
        true_i = i + 1
        if true_i not in index_value:
          print str(true_i),
   
