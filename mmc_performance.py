import subprocess
import sys
import re
import os
import time

#	total		use		 avalible
#['10327788  682844   9644944   7% /data']
def getAvalible():
	out = subprocess.check_output(['adb', 'shell', 'df'])
	match = re.findall(r'[0-9]+\s+[0-9]+\s+[0-9]+\s+[0-9]+%\s+/data', out)
	return match[0].split()

def showCurrentSpace():
	res = getAvalible()
	total = res[0]
	use = res[1]
	aval = res[2]
	usepercent = res[3]
	return "total:" + total + " use:" + use + " aval:" + aval + " percent:" + usepercent 
	
def root():
	retry = 10
	while retry:
		try:
			out = subprocess.check_output(['adb', 'root'])
			print out
			time.sleep(1)
			out = subprocess.check_output(['adb', 'remount'])
			print out
			retry = 0
		except:
			retry = retry - 1
			print "fail root or remount"

		
def reset():
	time.sleep(1)
	retry = 10
	while retry:
		try:
			out = subprocess.check_output(['adb', 'shell', 'echo 3 > /proc/sys/vm/drop_caches'])
			print out
			retry = 0
		except:
			retry = retry - 1
			print "fail reset"
	
def reboot():
	out = subprocess.check_output(['adb', 'shell', 'reboot'])
	
#[dev.bootcomplete]: [1]
def waitBootup():
	restrict = 150
	match = ''
	while restrict >= 0:
		try:
			out = subprocess.check_output(['adb', 'shell', 'getprop'])
			match = re.findall(r'\[dev.bootcomplete\]: \[1\]', out)
			if match:
				break
		except:
			print 'error'

		time.sleep(1)
		restrict = restrict - 1

	if match == '':
		print "boot fail"
	else:
		print "boot up"
	
#dd if=/dev/zero of=sun.txt bs=1M count=1
def fillTo(toPercent):
	res = getAvalible()
	total = int(res[0])
	use = int(res[1])
	aval = int(res[2])
	usepercent = res[3]
	size = (total * toPercent / 100 - use)/1024
	print size
	if size <= 0:
		return ''
	out = subprocess.check_output(['adb', 'shell', 'dd if=/dev/zero of=/data/fill%d.txt bs=1m count=%d' % (size, size)])
	return '/data/fill%d.txt' % (size)

def fillFinal(avaliable):
	res = getAvalible()
	total = int(res[0])
	use = int(res[1])
	aval = int(res[2])
	usepercent = res[3]
	size = (total - avaliable - use)/1024
	print size
	out = subprocess.check_output(['adb', 'shell', 'dd if=/dev/zero of=/data/fill%d.txt bs=1m count=%d' % (size, size)])
	return '/data/fill%d.txt' % (size)

def clear(filelist):
	for file in filelist:
		out = subprocess.check_output(['adb', 'shell', 'rm %s' % (file)])
		
def test1(bs):
	out = subprocess.check_output(['adb', 'shell', 'iozone -I -s 524288 -r %s -f /data/test%s -i 0 -i 1 -i 2' % (bs,bs)])
	pattern = "File stride size set to 17 * record size."
	str = out.find(pattern)
	return out[str + len(pattern):]

if __name__ == '__main__':

	tmpfile = []
	report = open("./emmctest%s.txt" % (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())), "w")
	
	report.write("emmc test report %s \n" % (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())))
	
	report.write("***********" + showCurrentSpace() + "***********\n")
	root()
	reset()
	res = test1('4')
	report.write(res)
	reset()
	time.sleep(20)
	res = test1('512')
	report.write(res)
	report.write('\n')
	
	tmpfile.append(fillTo(50))
	reboot()
	waitBootup()
	
	report.write("***********" + showCurrentSpace() + "***********\n")
	root()
	reset()
	res = test1('4')
	report.write(res)
	reset()
	time.sleep(20)
	res = test1('512')
	report.write(res)
	report.write('\n')
	
	tmpfile.append(fillTo(70))
	reboot()
	waitBootup()

	report.write("***********" + showCurrentSpace() + "***********\n")
	root()
	reset()
	res = test1('4')
	report.write(res)
	reset()
	time.sleep(20)
	res = test1('512')
	report.write(res)
	report.write('\n')
	reboot()
	waitBootup()
	
	tmpfile.append(fillTo(90))
	reboot()
	waitBootup()

	report.write("***********" + showCurrentSpace() + "***********\n")
	root()
	reset()
	res = test1('4')
	report.write(res)
	reset()
	time.sleep(20)
	res = test1('512')
	report.write(res)
	report.write('\n')

	tmpfile.append(fillFinal(1024*1024))
	reboot()
	waitBootup()

	report.write("***********" + showCurrentSpace() + "***********\n")
	root()
	reset()
	res = test1('4')
	report.write(res)
	reset()
	time.sleep(20)
	res = test1('512')
	report.write(res)
	report.write('\n')

	
	tmpfile.append(fillFinal(1024*700))
	reboot()
	waitBootup()

	report.write("***********" + showCurrentSpace() + "***********\n")
	root()
	reset()
	res = test1('4')
	report.write(res)
	reset()
	time.sleep(20)
	res = test1('512')
	report.write(res)
	report.write('\n')
	
	report.close()
	
	clear(tmpfile)