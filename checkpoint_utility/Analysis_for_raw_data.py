#! /usr/bin/env python


import os
import sys


class Analysis_for_raw_data:



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


 def Findout_validated_data_only( self, data_string_in_list, file_name_in ):
   count = 0
   rule_id = ''
   validated_data_list_in_list = []

   # Any handdle
   Any_value = "Any"
   if file_name_in != "./Raw_service_data.txt":
     Any_value ="0.0.0.0"

   for data_string in data_string_in_list:
      data_string_without_blank = data_string.strip()
      data_list = data_string_without_blank.split("\t")

      count = count + 1
      if len(data_list) == 0 or len(data_list) > 2:
        print "\" "+ str(count) +" \" is not proper data.!"
        sys.exit(0)     

      try:
       # first data is number
       interger_data = int(data_list[0])
       rule_id = int(interger_data)

       if len(data_list) == 2:
         if type(data_list[1]) == str and len(data_list[1]) > 0 and data_list[1] != '-':
           if data_list[1] == "Any":
             data_list[1] = Any_value
           validated_data_list_in_list.append(data_list)
       
      except:
       # first data is not number
       if len(data_list[0]) == 0 or data_list[0] == '-':
         pass
       else:
         if type(rule_id) == int:
           if data_list[0] == "Any":
              msg_list = [ str(rule_id), Any_value ]
           else:
              msg_list = [ str(rule_id), data_list[0] ]
           validated_data_list_in_list.append(msg_list)
         else:
           print "\" "+ str(count) +" \" is not good rule number.!"    
           sys.exit(0)

   return validated_data_list_in_list # def Findout_validated_data_only( self, data_string_in_list ):

 def Start( self ):

   file_name_list = ["./Raw_source_data.txt", "./Raw_destination_data.txt", "./Raw_service_data.txt"]
   for file_name_in in file_name_list:
      contents_lists = self.File_readlines_output_list(file_name_in)
      created_list_in_list =  self.Findout_validated_data_only(contents_lists, file_name_in)
      self.File_writelines( created_list_in_list, file_name_in )
      print file_name_in+" processing has been done!"



if __name__=="__main__":
 root_process= Analysis_for_raw_data()
 root_process.Start()
