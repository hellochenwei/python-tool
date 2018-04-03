from socket import *
from time import ctime
import subprocess

NOTEPAD = "D:\\Program Files\\Notepad++\\notepad++.exe"

HOST = '10.63.236.130'
#PORT = 21576
PORT = 27015
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def doNotepad(linuxFile):
	cmd = NOTEPAD + ' %s' % (linuxFile)
	print cmd
	out = subprocess.call(cmd)

while True:
	print 'waiting for connection...'
	tcpCliSock, addr = tcpSerSock.accept()
	print '...connected form :', addr

	while True:
		data = tcpCliSock.recv(BUFSIZ)
		if not data:
			break
		tcpCliSock.send('[%s] %s' % (ctime(), data))
		doNotepad(data)

	tcpCliSock.close()

tcpSerSock.close()