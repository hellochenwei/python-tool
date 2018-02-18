import subprocess
import sys
import re

class Node(object):
	def __init__(self, pfval, printVal, list, layer, isDir = False):
		self.parentVal = pfval
		self.printVal = printVal
		self.fullVal = self.parentVal + "/" + self.printVal
		self.childList = list
		self.childList2 = [self.fullVal + "/" + e[e.find(":") + 4:] for e in self.childList]
		self.childList3 = [e[e.find(":") + 4:] for e in self.childList]
		self.layer = layer
		self.isDir = isDir

def clean(list):
	for e in list:
		if e == "" or re.match(r'^total',e):
			list.remove(e)
	return list
	
def getchild(node):
	out = subprocess.check_output(['adb', 'shell', 'ls -l %s' % (node)])
	return clean(out.split('\r\n'))

def treeDir(node):
	if node.isDir is False:
		print node.layer * "\t" + "|---" + node.printVal
		return

	print node.layer * "\t" + "|---" + node.printVal
	
	for (fe, e, de) in zip(node.childList2, node.childList, node.childList3):
		isDir = False
		list = []
		if re.match(r'^d', e):
			list = getchild(fe)
			isDir = True
		else: 
			list = []

		node1 = Node(node.fullVal, de, list, node.layer + 1, isDir)
		#print node.fullVal, node.childList, node.childList2, node.childList3, node.isDir
		#print node1.childList, node1.printVal, node1.isDir, node1.layer
		treeDir(node1)
		

if	__name__ == '__main__':
	
	root = Node("", sys.argv[1], getchild(sys.argv[1]), 0, True)
	print root.childList, root.childList2, root.childList3, root.isDir
	treeDir(root)