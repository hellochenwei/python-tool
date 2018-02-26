import subprocess
import sys
import re
import threading
import time

# adb shell input keyevent 6 26

class RWThread (threading.Thread):
	def __init__(self, threadID, name, counter, file):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.file = file
	def run(self):
		while 1:
			out = subprocess.check_output(['adb', 'shell', 'iozone -I -s 1048576 -r 4k -f %s ' % (self.file)])

class ScreenThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		while 1:
			out = subprocess.check_output(['adb', 'shell', 'input keyevent 26'])
			#print "xxxxxx"
			time.sleep(2)
			out = subprocess.check_output(['adb', 'shell', 'input keyevent 6'])

if __name__ == '__main__':

	threads = []
	t4 = ScreenThread(4, "screen", 4)
	t1 = RWThread(1, "rw1", 1, "/data/test1")
	t2 = RWThread(2, "rw2", 2, "/data/test2")
	t3 = RWThread(3, "rw3", 3, "/data/test3")
	
	t1.start()
	t2.start()
	t3.start()
	t4.start()
	
	threads.append(t1)
	threads.append(t2)
	threads.append(t3)
	threads.append(t4)

	for t in threads:
		t.join()
