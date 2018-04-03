import bz2
import gzip
import sys
import os.path
import argparse
import re
import sqlite3
import datetime
import time
import string

class Unit(object):
	def __init__(self, time, tag, content):
		self.time = time
		self.tag = tag
		self.content = content

class ReadWriter(object):
	def __init__(self, read):
		self.writer = read + '/' + 'result.db'
		self.read = read

	def getWrite(self):
		self.conn = sqlite3.connect(self.writer)
		self.conn.text_factory = str
		self.csr = self.conn.cursor()
		
		try:
			create_cmd = 'CREATE TABLE Unit( \
						ttime NUMERIC, \
						ttag TEXT, \
						tmesg TEXT)'

			self.csr.execute(create_cmd)
		except:
			print "create fail"
			return ''
		
		list = os.listdir(self.read)
	
		for i in range(0, len(list)):
			if re.search(r'logcat_main|logcat_system|log_kernel', list[i], re.I):
				path = os.path.join(args.path,list[i])
				if os.path.isfile(path):
					print path
					if re.search(r'txt$', path, re.I):
						with open(path, 'rb') as f:
							for eachline in f:
								rw.write(eachline)
					elif re.search(r'gz$', path, re.I):
						with gzip.open(path, 'rb') as f:
							for eachline in f:
								rw.write(eachline)
					else:
						pass

	def write(self, msg):
		time = re.search(r'\d+-\d+\s+\d+:\d+:\d+\.\d+', msg)
		tag = re.search(r'\w\s\w+\s*:\s+|\[\d+: .*\]', msg)

			
		if time and tag:
			date_time = datetime.datetime.strptime(time.group(),'%m-%d %H:%M:%S.%f')
			self.csr.execute('INSERT INTO Unit VALUES (?,?,?)', 
					(date_time, tag.group(0), msg))
					
	def search(self, ltags):
		if ltags is None:
			cmd = 'SELECT tmesg FROM Unit ORDER BY ttime'
		else:
			pattern = ''
			for i in range(0, len(ltags) - 1):
				pattern = pattern + "ttag LIKE '%" + ltags[i] +"%'" + ' OR '	
			pattern = pattern + "ttag LIKE '%" + ltags[-1] + "%'"
			cmd = 'SELECT tmesg FROM Unit WHERE ' + pattern + ' ORDER BY ttime'
		print cmd
		self.csr.execute(cmd)
		for res in self.csr.fetchall():
			#ro.write("%s" % (res[0])
			print '%s' % (res[0]),


	def close(self):
		self.conn.commit()
		self.conn.close()

if __name__ == '__main__': 

	parser = argparse.ArgumentParser(description='Extract log according tags')
	parser.add_argument('--path', help='log path')
	parser.add_argument('--tags', nargs='*', help='tags')
	
	args = parser.parse_args()
	print args.path, args.tags
	
	rw = ReadWriter(args.path)
	rw.getWrite()
	rw.search(args.tags)

	rw.close()