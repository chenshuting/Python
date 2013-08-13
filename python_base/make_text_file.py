#!/usr/bin/python
import sys, os

if len(sys.argv) != 2:
	print "Usage:%s filename" % sys.argv[0]
	sys.exit(-1);

ls = os.linesep
filename = sys.argv[1];
print ls;

while True:
	if os.path.exists(filename):
		print "ERROR: '%s' already exists" % filename;
		filename = raw_input("new filename:>");
	else:
		break;

all = [];
print "\nEnter lines ('.' by itself to quit).\n";

while True:
	entry = raw_input('>');
	if entry == '.':
		break;
	else:
		all.append(entry);

fobj = open(filename, 'w');
fobj.writelines(["%s%s" % (x, ls) for x in all]);
fobj.close();
print 'DONE!';

