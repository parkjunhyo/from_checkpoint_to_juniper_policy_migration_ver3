#! /usr/bin/env python

import re

file_names = ["./service.renew"]
output_file_name = "./command_to_create_service_object.txt"

f = open(output_file_name,"w")
f.close()


duplicated_info = []
for file_name in file_names:

   f = open(file_name, "r")
   contents_in_file = f.readlines()
   f.close()


   for content_in_file in contents_in_file:

      _target_list_ = content_in_file.strip().split("\t")

      if len(_target_list_) == 2:
        [ policy_no, proto_type ] =content_in_file.strip().split("\t")
      elif len(_target_list_) == 3:
        [ policy_no, proto_type, _number_ ] =content_in_file.strip().split("\t")
      else:
        continue

      _re_proto_type_ = proto_type.lower()
      if re.search(_re_proto_type_,"icmp"):
        continue
      if re.search(_re_proto_type_,"any"):
        continue

      number_re = _number_.strip().split("-")
      number_sum = ""
      if len(number_re) == 1:
        number_sum = number_re[0]
      else:
        _temp_ = []
        for _ele_ in number_re:
           _temp_.append(_ele_)
        number_sum = "_".join(_temp_)
      application_name_lower = "%s_%s" % (_re_proto_type_,number_sum)
      application_name = application_name_lower.upper()

      number_re = _number_.strip().split("_")
      if len(number_re) != 1:
        _temp_ = []
        for _ele_ in number_re:
           _temp_.append(_ele_)
        application_number_range = "-".join(_temp_)
      else:
        application_number_range = number_re[0]

      if application_name not in duplicated_info:
        duplicated_info.append(application_name)
        f = open(output_file_name,"a")
        cli_command = "set applications application %s protocol %s source-port 0-65535 destination-port %s\n" % (application_name, proto_type.lower(), application_number_range)
        f.write(cli_command)
        f.close()
