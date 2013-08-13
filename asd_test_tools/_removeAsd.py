#!/usr/bin/python
import sys,math
sys.path.append("/usr/lib/asd")
from asd_lib import *; 

def USAGE():
	print "Usage:%s asd_name asd_size ap_name phydev_path";
	print "Usage:%s asd_num asd_size phydev_path[Node:default ap name:ap0]";
	sys.exit(-1);

def removeASD(asd_name, asd_size, ap_name, phy_path):
	phydev = PhyDev(phy_path);
	pool = AsdPool(ap_name, 16, phydev);
	asd = AsdDev(asd_name, asd_size, pool);
	asd.setInactive();
	asd.remove();
	
def removeASDList(asd_num, asd_size, phy_path):
	phydev = PhyDev(phy_path);
	pool = AsdPool("ap0", 16, phydev);
	asd_list = [AsdDev("asd%d" % x, asd_size, pool) for x in range(asd_num)];
	for asd in asd_list:
		asd.setInactive();
		asd.remove();
	
if len(sys.argv) == 4:
	removeASDList(string.atoi(sys.argv[1]), sys.argv[2], sys.argv[3]);
elif len(sys.argv) == 5:
	removeASD(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]);
else:
	USAGE();
