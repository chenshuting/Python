#!/usr/bin/python 
import sys,os
sys.path.append("/usr/lib/asd/");
from asd_util import *;

def USAGE():
	print "USAGE:Diff two file or two dirs"
	print "  %s path_1 path_2 output_file" % sys.argv[0];
	sys.exit(1);

def write_to_output(file, cmd):
	system("echo \"%s\" >> %s" % (cmd, file));

def diff(output_file, file1, file2):
	#start diff process
	system("diff -c -p %s %s >> %s" %(file1, file2, output_file));

def in_file_list(list, file):
	for path in list:
		if path == file:
			return 1;
	return 0;
	
def diff_dir_or_file(output_file, prefix1, prefix2, file):
	spath = "%s/%s" % (prefix1, file);
	dpath = "%s/%s" % (prefix2, file);
	if os.path.isdir(spath):
		diff_dirs(output_file, spath, dpath);
	else:
		diff(output_file, spath, dpath);
		
def diff_dirs(output_file, dir1, dir2):
	file_list_1 = os.listdir(dir1);
	file_list_2 = os.listdir(dir2);
	
#	diff(output_file, dir1, dir2);
	write_to_output(output_file, "Start diff directory:%s and %s" % (dir1,dir2));
	for file1 in file_list_1:
		if file1 == ".svn":
			continue;
		#search file 
		if file1 in file_list_2:
			diff_dir_or_file(output_file, dir1, dir2, file1);	
		else:
			write_to_output(output_file, "%s%s is added!" % (dir1, file1));

def start_process(output_file):
	if os.path.isfile(output_file):
		os.rename(output_file, "%s.bkp" % output_file);
	system("echo \"start test\" > %s" % output_file);

if len(sys.argv) != 4:
	USAGE();

path_1 = sys.argv[1];
path_2 = sys.argv[2];
output_file = sys.argv[3];

try:
	start_process(output_file);
	if os.path.isdir(path_1) and os.path.isdir(path_2):
		diff_dirs(output_file, path_1, path_2);	
	elif os.path.isfile(path_1) and os.path.isfile(path_2):
		diff(output_file, path_1, path_2);
	else:
		print "Error input! path_1 and path_2 must be the same type!";
except Exception,e:
	print e;

sys.exit(0);
