#! /usr/bin/env python

### read contents from orgin data
origin_data = "./Data/network_objects.data"
f = open(origin_data,"r")
read_contents = f.readlines()
f.close()

### output new objects table to use
output_data = "./network_objects.gen"

above_name = ""
above_type = ""

f = open(output_data,"w")

for read_content in read_contents:

  read_content_list = read_content.split("\t")

  object_name = read_content_list[0]
  object_type = read_content_list[1]

  # object name
  if object_name == "-":
    read_content_list[0] = above_name
  else:
    above_name = object_name

  # object type
  if object_type == "-":
    read_content_list[1] = above_type
  else:
    above_type = object_type

  # write the result
  line_to_write = "\t".join(read_content_list)
  f.write(line_to_write)

f.close()
