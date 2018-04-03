import socket
import select
import sys
import os

unixSerSocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
path = "./ltow"
if os.path.exists(path):  
   os.unlink(path)  
unixSerSocket.bind(path)
unixSerSocket.listen(5)
