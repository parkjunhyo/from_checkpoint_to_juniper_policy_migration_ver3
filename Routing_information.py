#! /usr/bin/env python

class Routing_information: 
 zone_name = ("pub","pri","com","pci")

 network_mask = { 
                  # public zone network  
                  zone_name[0]:(
                                "0.0.0.0/0",      # default
                                "150.183.0.0/16",
                                "150.197.0.0/16"
                               ),
                  # private zone network  
                  zone_name[1]:(
                                "70.12.204.0/24",
                                "70.12.206.0/24",
                                "70.12.201.0/24",
                                "70.12.203.0/24",
                                "70.12.202.0/24",
                                "203.235.207.0/24",
                                "203.235.205.0/24",
                                "192.168.0.0/16",
                                "172.16.0.0/12",
                                "150.0.0.0/8",
                                "10.0.0.0/8"
                               ),
                  # commerce zone network  
                  zone_name[2]:(
                                "172.22.232.0/24",
                                "172.22.193.0/24",
                                "172.22.192.0/24",
                                "172.22.195.0/24",
                                "172.22.194.0/24",
                                "172.22.197.0/24",
                                "172.22.196.0/24",
                                "172.22.198.0/24",
                                "172.22.201.0/24",
                                "172.22.200.0/24",
                                "172.22.203.0/24",
                                "172.22.202.0/24",
                                "172.22.205.0/24",
                                "172.22.204.0/24",
                                "172.22.206.0/24",
                                "172.22.116.0/24",
                                "172.22.118.0/24",
                                "172.22.119.0/24",
                                "172.22.112.0/24",
                                "172.22.113.0/24",
                                "172.22.114.0/24",
                                "172.22.115.0/24",
                                "172.22.124.0/24",
                                "172.22.120.0/24",
                                "172.22.121.0/24",
                                "172.22.122.0/24",
                                "172.22.123.0/24",
                                "172.22.237.0/27",
                                "172.22.237.32/27",
                                "172.22.237.64/27",
                                "172.22.237.96/27"
                               ),
                  # pci-dss zone network  
                  zone_name[3]:(
                                "172.22.117.0/24",
                                "172.22.125.0/24",
                                "172.22.199.0/24",
                                "172.22.207.0/24"
                               )  
                }

 juniper_info = {
                  #"device_ip":"159.203.103.72",
                  "device_ip":"211.206.101.100",
                  "username":"root",
                  #"password":"Start@1sk"
                  "password":"jun2per"
                }
 
 command_mode = "test"    # "real" or "test"