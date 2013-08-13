#!/usr/bin/python
import sys,math
sys.path.append("/usr/lib/asd")
from asd_lib import *; 

def USAGE():
	print "Usage:%s ap_name granual phy_path [phy_path...]";
	print "Usage:%s phy_path [phy_path] [Node:default granual:16, ap name:ap0]";
	sys.exit(-1);

def createPool(ap_name, granual, phy_path):
	system("asdpoolcreate -n %s -g %s %s" % 
		(ap_name, granual, phy_path));
	
if len(sys.argv) < 4:
	USAGE();
else:
	len = len(sys.argv);
	phy_path = "";
	for x in range(3,len):
		phy_path += "%s " % sys.argv[x];	
	createPool(sys.argv[1], string.atoi(sys.argv[2]), phy_path);
