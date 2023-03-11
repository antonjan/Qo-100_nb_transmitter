#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from xmlrpc.client import ServerProxy
import time
xmlrpc_control_client = ServerProxy('http://192.168.10.96:8008')
xmlrpc_control_client.set_ptt(1)


#import xmlrpclib
#import time
# this programm calls gnuradio and sets the PTT verable to 1 for tx
#s = xmlrpclib.Server('http://localhost:8008')
#s.set_freq(1000)
#s.set_ptt(0)
