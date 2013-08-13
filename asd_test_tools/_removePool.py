#!/usr/bin/python
import sys,math
sys.path.append("/usr/lib/asd")
from asd_lib import *; 

def USAGE():
	print "Usage:%s ap_name granual phy_path";
	print "Usage:%s phy_path [Node:default granual:16, ap name:ap0]";
	sys.exit(-1);

def removePool(ap_name, granual, phy_path):
	phydev = PhyDev(phy_path);
	pool = AsdPool(ap_name, granual, phydev);
	pool.setInactive();
	pool.remove();
	
if len(sys.argv) == 1:
	USAGE();
elif len(sys.argv) == 2:
	removePool("ap0", 16, sys.argv[1]);
elif len(sys.argv) < 4:
	USAGE();
else:
	removePool(sys.argv[1], string.atoi(sys.argv[2]), sys.argv[3]);
