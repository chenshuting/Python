#!/usr/bin/python
import sys
import os 
import string
import threading
from subprocess import Popen, PIPE, STDOUT

ASSERTION_FAILED = "[Assertion failed] ";
PROP_CLEAN = 0;
PROP_DIRTY = 1;
PROP_UMAP = 2;

def minor(dev):
	cmdRet = system("ls -l %s" % dev);
	return int(cmdRet.stdout.split(" ")[5])

def enter(str=""):
	print "------ enter file:%s ------" % sys.argv[0];
	print str;
	sys.stdout.flush();

def leave(str=""):
	print str;
	print "------ leave file:%s ------" % sys.argv[0];
	sys.stdout.flush();

def gcd(x, y):
	if x < y:
		gcd(y,x);
	if (x & 0x01) == 0 and (y & 0x01) == 0:
		return 2 * gcd(x >> 1,y >> 1);
	elif (x & 0x01) and (y & 0x01):
		return gcd(y, x-y);
	elif (x & 0x01) == 0:
		return gcd(y, x >> 1);
	else:
		return gcd(x, y >> 1);

class ColoredStr:
	def __init__(self, str):
		self.str = str;

	def toGray(self):
		return "\033[30;1m%s\033[m" % self.str;

	def toRed(self):
		return "\033[31;1m%s\033[m" % self.str;

	def toGreen(self):
		return "\033[32;1m%s\033[m" % self.str;

	def toYellow(self):
		return "\033[33;1m%s\033[m" % self.str;

	def toBlue(self):
		return "\033[34;1m%s\033[m" % self.str;

	def toBlue(self):
		return "\033[34;1m%s\033[m" % self.str;

ASSERTION_FAILED = "[%s] " % ColoredStr("Assertion failed").toRed();

def eachSmallRange(start, end, step):
	if (start < end and step > 0):
		while end - start > step:	
			yield (start, start + step);
			start = start + step;
		yield (start, end);

class MultiTask:
	def __init__(self):
		self.threads = [];
		self.processes = [];
		self.threadCnt = 0;
		self.processCnt = 0;

	def __del__(self):
		self.removeThreads();
		self.removeProcess();

	def createThread(self, func, *args):
		t = threading.Thread(func, *args);
		print "Thread:%s is create" % ColoredStr("%s" % t.getName()).toYellow();
		return t;

	def addThread(self, func, args=()):
		t = self.createThread(func, *args); 
		self.threads.append(t);
		self.threadCnt = self.threadCnt + 1;
		return t;

	def threadPool(self, thread_num, func, args=()):
		for i in xrange(0, thread_num):
			t = self.addThread(func, *args);
	
	def runThreads(self):
		for t in self.threads:
			t.start();

	def waitThreads(self):
		for t in self.threads:
			t.join();
			print "Thread:%s is done!" % ColoredStr("%s" % t.getName()).toYellow();
			self.threadCnt = self.threadCnt - 1;

	def removeThreads(self):
		if self.threadCnt > 0:
			self.waitThreads();
		for t in self.threads:
			self.threads.remove(t);
		self.threadCnt = 0;

	def createProcess(self, func, *args):
		pid = os.fork();
		if pid == 0:
			func(*args);
			os._exit(0);
		else:
			return pid;
	
	def addProcess(self, func, args = ()):
		pid = self.createProcess(func, *args);
		print "Process:%s is start!" % ColoredStr("%d" % pid).toYellow();
		self.processes.append(pid);
		self.processCnt = self.processCnt + 1;
		return pid;
		
	def waitProcess(self):
		for pid in self.processes:
			(cpid, status) = os.waitpid(pid, 0);
			print "process:%s is done!" % ColoredStr("%d" % pid).toYellow();
			if status != 0:
				lastCmdExitcode = status;
			self.processCnt = self.processCnt - 1;

	def processPool(self, num):
		global lastCmdExitcode;
		if self.processCnt > 0:
			self.waitProcess();	
		for i in xrange(0, num):
			pid = os.fork();
			if pid == 0:
				yield i;
				os._exit(lastCmdExitcode);
			elif pid > 0:
				self.processes.append(pid);
			else:
				assert 0;
		self.waitProcess();

	def removeProcess(self):
		if self.processCnt > 0:
			self.waitProcess();
		for pid in self.processes:
			self.processes.remove(pid);
		self.processCnt = 0;

class Cmd:
	def __init__(self, cmd):
		self.exitcode = 0;
		self.stdout = "";
		self.stderr = "";
		self.cmd = cmd;

lastCmdExitcode = 0;

class system(Cmd):
	def __init__(self, cmd):
		global lastCmdExitcode;
		Cmd.__init__(self, cmd);
		print "\ncommand: %s" % ColoredStr(cmd).toGreen();
		pipe = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE);
		out = pipe.communicate();
		self.exitcode = pipe.wait();
		lastCmdExitcode = self.exitcode;
		if self.exitcode != 0:
			print "exitcode: %s" % ColoredStr(self.exitcode).toRed();
		else:
			print "exitcode: %d" % self.exitcode;
		self.stdout = out[0];
		print "stdout:" 
		print self.stdout
		if self.exitcode != 0:
			self.stderr = out[1];
			print "stderr:"
			print ColoredStr(self.stderr).toRed();
		sys.stdout.flush();
		sys.stderr.flush();

class PhyDev:
	def __init__(self, path):
		self.path = path

	def clearHead(self):
		cmdRet = system("dd if=/dev/zero of=%s bs=54M count=1 oflag=direct" %
				self.path)
		return cmdRet;

	def minor(self):
		cmdRet = system("ls -l %s" % self.path);
		return int(cmdRet.stdout.split(" ")[5])

	def align_dd(self, bs, count, seek=0):
		seekStr = "";
		if (seek != 0):
			seekStr = "seek=%d" % seek;

		cmdRet = system("dd if=/dev/zero of=%s bs=%s count=%d %s oflag=direct" %
				(self.path, bs, count, seekStr));
		return cmdRet;

	def noalign_dd(self, bs, count, seek=0):
		seekStr = "";
		if (seek != 0):
			seekStr = "seek=%d" % seek;

		cmd = "dd if=/dev/zero of=%s bs=%s count=%d %s" % (
				self.path, bs, count, seekStr);
		cmdRet = system(cmd);
		return cmdRet;

class LvmVg:
	def __init__(self, name):
		self.name = name;

	def createLv(self, lv):
		lv.vg = self;
		lv.path = "/dev/%s/%s" % (self.name, lv.name);
		cmd = system("lvcreate -n %s -L %s %s" % (lv.name, lv.size, self.name));
		return cmd;

	#no remove method
	def scan(self):
		cmdRet = system("lvscan");
		return cmdRet.stdout;

	def allLvPath(self):
		lvscanOutput = self.scan();
		for i in lvscanOutput.strip().split('\n'):
			yield i.split()[1].split('\'')[1];

	def pathsOfLvs(self):
		lvsPath = [i for i in self.allLvPath() if i.split("/")[2] == self.name];
		return " ".join(lvsPath);

class LvmLv(PhyDev):
	def __init__(self, name, size="", vg=None):
		if vg:
			PhyDev.__init__(self, "/dev/%s/%s" % (vg.name, name));
		else:
			PhyDev.__init__(self, "/dev/null");
		self.vg = vg;
		self.name = name;
		self.size = size;

	def remove(self):
		return system("lvremove -f /dev/%s/%s" % (self.vg.name, self.name));

class _Gbdt:
	def __init__(self):
		kernel_src_path = ""

	
	def shortTermTest(self, asd):
		return system("gbdtrun -m S -p %s" % asd.path)	

Gbdt = _Gbdt();

