#!/usr/bin/python
import sys
import os
import time

if (len(sys.argv) < 2):
	print "Usage: ./filename param1 param2 ..."
	sys.exit(0);
	

filename = sys.argv[1];

start = time.time();
print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())); 

os.system("./%s" % filename);

end = time.time();
print "Now: %s ~~~~~~" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))); 
diff = end-start;
print "Using time:%f s" % diff;
