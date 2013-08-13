#!/usr/bin/python 
import sys
sys.path.append("/usr/lib/asd");
from asd_lib import *;

def USAGE():
	print "Usage: %s 0 asd_name bs count   --- dd fixed bs and count" % sys.argv[0];
	print "Usage: %s 1 asd_name asd_size count  --- dd all" % sys.argv[0];
	print "Usage: %s 2 asd_name asd_size process_num --- dd all with multiple process" % sys.argv[0];
	print "Usage: %s 3 asd_name bs length interval --- dd fixed bs and count with interval" % sys.argv[0];
	sys.exit(-1);
	
def dd_Dev(asd_name, bs, count):
	system("dd if=/dev/zero of=/dev/%s bs=%s count=%d oflag=direct" % 
		(asd_name, bs, count));

def dd_with_interval(asd_name, bs, length, interval):
	for x in range(length):
		index = 2 * interval; 
		system("dd if=/dev/zero of=/dev/%s bs=%s count=1 seek=%s oflag=direct" % 
			(asd_name, bs, index));

def dd_all(asd_name, asd_size, count):
	for loop in range(count):
		length = asd_size; #size unit:MB
		for seek in range(length):
			system("dd if=/dev/zero of=/dev/%s bs=1M count=1 seek=%d oflag=direct"
				% (asd_name, seek));	
	
def dd_with_multitask(asd_name, asd_size, process_num):
	count = asd_size / 4; #size unit:KB
	for pid in processPool(process_num):
		for x in range(count):
			system("dd if=/dev/zero of=/dev/%s bs=4K count=1 seek=%d oflag=direct"
				% (asd_name, x));	
	

if len(sys.argv) < 4:
	USAGE();

type = string.atoi(sys.argv[1]);
len = len(sys.argv);
asd_name = sys.argv[2];

if type == 0 and len == 5:
	bs = sys.argv[3];
	count = string.atoi(sys.argv[4]);
	dd_Dev(asd_name, bs, count);
elif type == 1 and len == 5:
	asd_size = string.atoi(sys.argv[3]);
	count = string.atoi(sys.argv[4]);
	dd_all(asd_name, asd_size, count);
elif type == 2 and len == 5:
	asd_size = string.atoi(sys.argv[3]);
	process_num = string.atoi(sys.argv[4]);
	dd_with_multitask(asd_name, asd_size, process_num);
elif type == 3 and len == 6:
	bs = sys.argv[3];
	length = string.atoi(sys.argv[4]);
	interval = string.atoi(sys.argv[5]);
	dd_with_interval(asd_name, bs, length, interval);
else:
	USAGE();
	
