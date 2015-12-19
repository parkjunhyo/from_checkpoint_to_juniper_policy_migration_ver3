#! /usr/bin/env python

from Routing_information import Routing_information
from Utility_function import Utility_function

import sys, time, os
from netaddr import *
import paramiko

class SSH_login_get_information(Routing_information):

  output_msg = ""

  Upper_capital_zone_name=[]
  policy_name_in_device=[]

  def __init__( self ):

     os.system("rm -rf ./policy_from_juniper_device.txt")

     # change Upper letter
     for name_z in self.zone_name:
        if name_z.upper() not in self.Upper_capital_zone_name:
          self.Upper_capital_zone_name.append(name_z.upper())
 

  def Open_ssh_device( self ):
     remote_conn_pre = paramiko.SSHClient()
     remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

     # connet with ip, username and password
     remote_conn_pre.connect(self.juniper_info["device_ip"],
                             username=self.juniper_info["username"],
                             password=self.juniper_info["password"],
                             look_for_keys=False,
                             allow_agent=False)
     time.sleep(5)
     remote_conn = remote_conn_pre.invoke_shell()
     time.sleep(1)
     # return value
     return remote_conn_pre, remote_conn 

  def Close_ssh_device( self, remote_conn_pre, remote_conn ):
     remote_conn.close()
     remote_conn_pre.close()

  def _re_write_( self, msg_input ):
     # because of juniper output is not proper,
     # blank character is issue
     file_f = open("./temp_ssh_result.txt","w")
     file_f.write(msg_input)
     file_f.close()

     file_f = open("./temp_ssh_result.txt")
     contents = file_f.readlines()
     file_f.close()
     os.system("rm -rf ./temp_ssh_result.txt")
     return contents 


  def _exchange_string_from_list_( self, input_list ):
     return ";".join(input_list)

  def _extract_net_( self, input_list ):
     return_result = []
     for in_string in input_list:
        in_string.strip()
        splited_in_string = in_string.split()
        return_result.append(splited_in_string[1].strip())
     return return_result

  def _transfer_command_( self, remote_conn, mode, command ):
     # mode = "real" : real device command
     if mode != "real":
       # command send and get information
       remote_conn.send("cli\n") 
       time.sleep(1)
       remote_conn.recv(2000)

       remote_conn.send(command) 
       time.sleep(5)
       return_result = remote_conn.recv(10000000)

       remote_conn.send("exit\n") 
       time.sleep(1)
       remote_conn.recv(2000)

       remote_conn.send("exit\n") 
       time.sleep(1)
       remote_conn.recv(2000)

     else:
       print "this is real command!"
       sys.exit(0)
     # mode = "real" : real device command
     return return_result
      


  def Start( self ):
  
     # connect network devices 
     remote_conn_pre, remote_conn = self.Open_ssh_device()

     # command send and get information to find "policy name"
     j_command = "show security policies hit-count | no-more\n"
     self.output_msg = self._transfer_command_( remote_conn, self.command_mode, j_command )

     # dis-connect network devices
     self.Close_ssh_device(remote_conn_pre, remote_conn)

     # print out with file and re write contents
     contents = self._re_write_(self.output_msg)

     # find_out policy name
     policy_name_in_device=[]
     for string_contents in contents:
        string_contents.strip()
        splited_contents = string_contents.split()

        if len(splited_contents) == 5:
          if (splited_contents[1].upper() in self.Upper_capital_zone_name) and (splited_contents[2].upper() in self.Upper_capital_zone_name):
            if splited_contents[3] not in self.policy_name_in_device:
              self.policy_name_in_device.append(splited_contents[3])

     f_count = 0
     for p_name in self.policy_name_in_device:
        j_command = "show security policies policy-name %s detail | no-more\n" % (p_name)

        # connect network devices
        remote_conn_pre, remote_conn = self.Open_ssh_device()
 
        # command send and get information
        self.output_msg = self._transfer_command_( remote_conn, self.command_mode, j_command )

        # dis-connect network devices
        self.Close_ssh_device(remote_conn_pre, remote_conn)

        # print out with file and re write contents, ***** main result *****
        contents = self._re_write_(self.output_msg)

        # findout the index number to match
        index_counting = 0
        application_index = None
        for strings in contents:
           strings.strip()
           # zone name information
           if "From zone:" in strings and "To zone:" in strings:
             from_to_zone_index = int(index_counting)
             index_counting = index_counting + 1
             continue
           # source address start
           if "Source addresses:" in strings:
             source_net_index = int(index_counting)
             index_counting = index_counting + 1
             continue
           # destination address start
           if "Destination addresses:" in strings:
             destination_net_index = int(index_counting)
             index_counting = index_counting + 1
             continue
           # application start
           if "Application:" in strings:
             if not application_index:
               application_index = int(index_counting)
               index_counting = index_counting + 1
               break
           # increase count
           index_counting = index_counting + 1

        # findout from zone and to zone
        contents[from_to_zone_index].strip()
        splited_zone_name = contents[from_to_zone_index].split(",")
        fromzone_name = splited_zone_name[0].split()[-1]
        tozone_name = splited_zone_name[-1].split()[-1]
      
        # source and destination network
        sourcenet_list = self._extract_net_(contents[(source_net_index+1):destination_net_index])       
        destnationnet_list = self._extract_net_(contents[(destination_net_index+1):application_index])       

        # application infomation
        index_counting = 0
        application_start_group = []
        for strings in contents:
           strings.strip()
           if "Application:" in strings:
             application_start_group.append(int(index_counting))
           index_counting = index_counting + 1
        application_port_list = []             
        for i_ in application_start_group:
           # application_name
           app_name = contents[i_].split()[-1]
           # application protocol
           protocol_line = contents[i_+1].split(",")
           app_proto = protocol_line[0].split()[-1]
           app_timeout = protocol_line[-1].split()[-1]
           # dest port
           port_range_string = contents[i_+3].split()[-1]
           remove_str = port_range_string.split("[")[-1]
           app_port = remove_str.split("]")[0]
           # create string
           insert_msg = "%s|%s|%s|%s" % (app_name,app_proto,app_port,app_timeout)
           application_port_list.append(str(insert_msg))

        # rule policy name infomation
        matched_seq_no = p_name.split("_")[0] 
        
        # print out the result on monitor
        f_count = f_count + 1
        print "policy name [ %s ] has been done... %s/%s" % (p_name, f_count, str(len(self.policy_name_in_device)))
        # print out the result as file
        str_src = self._exchange_string_from_list_(sourcenet_list)
        str_dst = self._exchange_string_from_list_(destnationnet_list)
        str_app = self._exchange_string_from_list_(application_port_list)

        file_o = open("./policy_from_juniper_device.txt","a")
        output_msg = "%s\t %s\t %s\t %s\t %s\t %s\n" % (str(matched_seq_no), fromzone_name, str_src, tozone_name, str_dst, str_app)
        file_o.write(output_msg)
        file_o.close()



if __name__=="__main__":
 root_process= SSH_login_get_information()
 root_process.Start()
