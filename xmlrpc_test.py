#install xmlrpclib
#import xmlrpclib
#import time
# This program set the ptt verable in gnuradio to 0
#s = xmlrpclib.Server('http://192.168.10.96:8008')
#s.set_freq(1000)
#s.set_ptt(0)

import time
import xmlrpc.client
s = xmlrpc.client.ServerProxy('http://192.168.10.96:8008')
print("ptt off")
print(s.set_ptt(0))
time.sleep(5)
print("ptt on")
print(s.set_ptt(1))
# Print list of available methods
#print(s.system.listMethods())
