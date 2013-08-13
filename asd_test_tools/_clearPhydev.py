#!/usr/bin/python 
import sys
sys.path.append("/usr/lib/asd");
from asd_util import *;

dev_num = len(sys.argv);
if dev_num <= 1:
	print "Usage: %s phydev1 [phydev2]" % sys.argv[0];
	sys.exit(-1);
print "Clear phydev....";

for x in range(1,dev_num):
	phydev = PhyDev(sys.argv[x]);
	phydev.clearHead();

print "Finish clear phydev....";

