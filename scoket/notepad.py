#!/usr/bin/env python

from socket import *
from time import ctime
import os
import sys

HOST = '10.63.236.130'
#PORT = 21576
PORT = 27015
BUFSIZ = 1024
ADDR = (HOST, PORT)

def getFullName(file):
	if file[0] is '/':
		return file
	
	cur = os.getcwd()
	cur = '/' + cur + '/' + file
	res = cur.replace('home', '10.41.98.23')
	res1 = res.replace('/', '\\')
	return res1

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


data = sys.argv[1]
#if not data:
#	break
res = getFullName(data)
tcpCliSock.send(res)
data = tcpCliSock.recv(BUFSIZ)
#if not data:
#	break
print data

tcpCliSock.close()
