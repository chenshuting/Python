#!/usr/bin/python
import sys
import os
import random

if (len(sys.argv) != 4):
	print "Usage:./%s outputfile number boundary" % sys.argv[0];
	sys.exit(0);
	
output_path=sys.argv[1]
number=int(sys.argv[2]);
boundary=int(sys.argv[3]);
i = 0;

if (number < 0 or boundary < 0):
	print "Error param: number=%d, boundary=%d" % (numbers,boundary);
	
print "generate %d of int numbers smaller than %d" % (number, boundary);

while (i < number) :
	i = i + 1;
	os.system("echo %d >> %s" % (random.randint(0,boundary), output_path));
