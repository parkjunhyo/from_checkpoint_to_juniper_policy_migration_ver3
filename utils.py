#! /usr/bin/env python

def findDefaultzone(zone_names_list, netmask_list ):
   default_zone_name = ""
   for zone_name in zone_names_list:
       if "0.0.0.0/0" in netmask_list[zone_name]:
          default_zone_name = zone_name 
       else:
          continue
   return default_zone_name



