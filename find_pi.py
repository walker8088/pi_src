#!/usr/bin/env python 
# -*- coding:UTF-8 -*-

from socket import *
from time import ctime

HOST = '127.0.0.1'
PORT = 21578
BUFSIZE = 1024

ADDR = (HOST,PORT)

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind(('',PORT))

print 'finding my pi...'
try:
    while True:
	data, addr = sock.recvfrom(BUFSIZE)
	print('recv from %s : %s'%(addr[0],data))
except:
    pass
sock.close()