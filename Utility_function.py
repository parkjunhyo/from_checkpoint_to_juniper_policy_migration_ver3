#! /usr/bin/env python

class Utility_function:

 def Read_file( self, file_name ):
  f = open( file_name )
  contents = f.readlines()
  f.close()
  return contents

 def addressInNetwork(self, ip, net):
   import socket,struct
   ipaddr = int(''.join([ '%02x' % int(x) for x in ip.split('.') ]), 16)
   netstr, bits = net.split('/')
   netaddr = int(''.join([ '%02x' % int(x) for x in netstr.split('.') ]), 16)
   mask = (0xffffffff << (32 - int(bits))) & 0xffffffff
   return (ipaddr & mask) == (netaddr & mask)





