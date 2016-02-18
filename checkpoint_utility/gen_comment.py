#! /usr/bin/env python

import re

### read contents from orgin data
origin_data = "./Data/comment.data"
f = open(origin_data,"r")
read_contents = f.readlines()
f.close()

### output new objects table to use
output_data = "./comment.gen"

above_name = ""
above_type = ""


numbering = []
f = open(output_data,"w")

for read_content in read_contents:

  read_content_list = read_content.strip().split("\t")

  object_number = read_content_list[0]
  object_comment_string = read_content_list[1]


  if re.match("[0-9]+",object_number):
    if int(object_number) not in numbering:
      numbering.append(int(object_number))
      if object_comment_string == "-":
        continue
      else:
        msg_string = "\t".join([object_number, object_comment_string])
      f.write(msg_string+"\n")
  else:
    continue


f.close()
