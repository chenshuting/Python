#!/usr/bin/python
import sys, os, string
from asd_util import *
from subprocess import Popen, PIPE, STDOUT

conf_dict = { 19 : (1<<12), 16 : (1<<9), 12 : (1<<5)} # TODO: fill the dictionary

BWC_SET_BLKS_ATTR = 0x00
BWC_GET_BLKS_ATTR = 0x01
BWC_GET_VALID_BLKS = 0x02
BWC_GET_SETBLKS_RESULT = 0x03
BWC_CLEAR_SETBLKS_RESULT = 0x04
BWC_TEST_SETBLKS_RESULT = 0x05

class Check:
	def __init__(self):
		self.stat_prefix = "statistic";	

class AsdCheck(Check):
	def __init__(self, asd_name, pool_name):
		Check.__init__(self);
		self.asd_name = asd_name;
		self.pool_name = pool_name;
	
	def save_statistic(self, save_path, num):
		result_path = "%s/%s_%s_%d" % (save_path, self.stat_prefix, self.asd_name, num);
		os.system("cp /proc/asd/%s/%s/asdinfo %s" % (self.pool_name, self.asd_name, result_path));

	def cmp_stat(self, save_path, num1, num2):
		asd_stat_1 = "%s/%s_%s_%d" % (save_path, self.stat_prefix, self.asd_name, num1);
		asd_stat_2 = "%s/%s_%s_%d" % (save_path, self.stat_prefix, self.asd_name, num2);
		cmp_result = "%s/stat_cmp_%s_%d_%d" % (save_path, self.asd_name, num1, num2);
		os.system("diff %s %s | tee %s" % (asd_stat_1, asd_stat_2, cmp_result));

class PoolCheck(Check):
	def __init__(self, pool_name):
		Check.__init__(self);
		self.pool_name = pool_name;
		self.bitmap_str = "bitmap_for_%s" % self.pool_name;
		self.map_str = "map_for_%s" % self.pool_name;

	def save_statistic(self, save_path, num): 
		result_path = "%s/%s_%s_%d" % (save_path, self.stat_prefix, self.pool_name, num);
		os.system("cp /proc/asd/%s/poolinfo %s" % (self.pool_name, result_path)); 

	def cmp_stat(self, save_path, num1, num2):
		ap_stat_1 = "%s/%s_%s_%d" % (save_path, self.stat_prefix, self.pool_name, num1);
		ap_stat_2 = "%s/%s_%s_%d" % (save_path, self.stat_prefix, self.pool_name, num2);
		cmp_result = "%s/stat_cmp_%s_%d_%d" % (save_path, self.pool_name, num1, num2);
		os.system("diff %s %s | tee %s" % (ap_stat_1, ap_stat_2, cmp_result));

	def save_display_info(self, save_path, num):
		result_path = "%s/%s_%d" % (save_path, self.stat_prefix, num);
		os.system("asdpooldisplay -n %s | tee %s" % self.pool_name, result_path);

	def get_dev_num(self):
		cmdRet = system("asdpooldisplay -c -n %s" % self.pool_name);	
		return int(cmdRet.stdout.split(":")[2]);

	def get_user_asd_num(self):
		dev_num = self.get_dev_num();
		return (dev_num - 2) / 2;

	def get_pfbb_bitmap(self, save_path, prefix, count):
		phy_pfbb_path = "%s/%s_%s_%d" % (save_path, prefix, self.bitmap_str, count);
		system("_get-used-blocks-from-pfbb-info.sh %s 0 > %s" % (save_path, phy_pfbb_path));

	def get_dev_maps(self, save_path, prefix, count):
		asd_map_path = "%s/%s_%s_%d" % (save_path, prefix, self.map_str, count);
		user_asd_num = self.get_user_asd_num();
		system("_get-used-blocks-from-map-info.sh %s %d > %s" % (save_path, user_asd_num, asd_map_path));

	def self_res_check(self, save_path, count):
		self_check_file = "res_check_%s" % self.pool_name;
		#asd pool resource self check
		system("echo a > /proc/asd/%s/poolinfo" % pool.name);
		#save check result
		system("cp /tmp/%s %s/%s_%d" % (self_check_file, save_path, self_check_file, count));

	def cmp_bitmap_with_map(self, save_path, prefix, map_cnt, pfbb_cnt):
		asd_map_path = "%s/%s_%s_%d" % (save_path, prefix, self.map_str, map_cnt);
		phy_pfbb_path = "%s/%s_%s_%d" % (save_path, prefix, self.bitmap_str, pfbb_cnt);
		#compare two files complementaryly
		ret = system("diff %s %s | tee %s/%s_cmp_pfbb%d_and_map%d" % 
			(asd_map_path, phy_pfbb_path, save_path, prefix, pfbb_cnt, map_cnt)).exitcode;
		if ret == 0:
			print "Compare pfbb with map SUCCESS!!~~~~~O(^_^)O~~~~~";
		else:
			print "Compare pfbb with map FAILED!!....~o(u_u)o~...."     

	def cmp_map(self, save_path, prefix, num1, num2):
		map_1 = "%s/%s_%s_%d" % (save_path, prefix, self.map_str, num1);
		map_2 = "%s/%s_%s_%d" % (save_path, prefix, self.map_str, num2);
		result_path = "%s/cmp_%s_%d_%d" % (save_path, self.map_str, num1, num2);
		return system("diff %s %s | tee %s" % (map_1, map_2, result_path)).exitcode;

class SysCheck(Check):
	def __init__(self):
		Check.__init__(self);

	def save_statistic(self, save_path, num):
		result_path = "%s/%s_sys_%d" % (save_path, self.stat_prefix, num);
		os.system("cp /proc/asd/sysinfo %s" % result_path);

	def cmp_stat(self, save_path, num1, num2):
		sys_stat_1 = "%s/%s_sys_%d" % (save_path, self.stat_prefix, num1);
		sys_stat_2 = "%s/%s_sys_%d" % (save_path, self.stat_prefix, num2);
		cmp_result = "%s/stat_cmp_sys_%d_%d" % (save_path, num1, num2);
		os.system("diff %s %s | tee %s" % (sys_stat_1, sys_stat_2, cmp_result));	

class AsdDev(PhyDev, AsdCheck):
	def __init__(self, name, size="", pool=None):
		PhyDev.__init__(self, "/dev/%s" % name);
		AsdCheck.__init__(self, name, pool.name);
		self.name = name;
		self.size = size;
		self.pool = pool;
		self.path = "/dev/%s" % name; 
	
	#display info
	def displayInColonFormat(self):
		cmd = "asddisplay -c %s" % self.name;
		return system(cmd);

	def displayBriefly(self):
		cmd = "asddisplay -s %s" % self.name;
		return system(cmd);

	def display(self):
		cmd = "asddisplay %s" % self.name;
		return system(cmd);
	
	#change status
	def setInactive(self):
		cmd = "asdchange -a n %s" % self.name;
		return system(cmd);

	def setActive(self):
		cmd = "asdchange -a y %s" % self.name;
		return system(cmd);

	def remove(self):
		cmd = "asdremove -f %s" % self.name;
		return system(cmd);

	def extend(self,extendSize=""):
		cmd = "asdextend -L %s %s" % (extendSize,self.name);
		return system(cmd);

	def align_dd(self, bs, count, seek=0):
		seekStr = "";
		if (seek != 0):
			seekStr = "seek=%d" % seek;

		cmdRet = system("dd if=/dev/zero of=%s bs=%s count=%d %s oflag=direct" %
				(self.path, bs, count, seekStr));
		return cmdRet;



	#unmap/remap related
	def syncRemapFromSrc(self, src, start, len):
		asdMinor = minor("/dev/%s" % src.name);
		cmd = system("echo r%d:%d:%d:1 > /proc/asd/%s/%s/asdinfo" % ( 
					   asdMinor, start, len, self.pool.name, self.name));
		return cmd;
       
	def syncRemapToDst(self, dst, start, len):
		asdMinor = minor("/dev/%s" % self.name);
		cmd = system("echo r%d:%d:%d:1 > /proc/asd/%s/%s/asdinfo" % ( 
					   asdMinor, start, len, self.pool.name, dst.name));
		return cmd;
       
	def asyncRemapFromSrc(self, src, start, len):
		asdMinor = minor("/dev/%s" % src.name);
		cmd = system("echo r%d:%d:%d > /proc/asd/%s/%s/asdinfo" % ( 
					   asdMinor, start, len, self.pool.name, self.name));
		return cmd;

	def asyncRemapToDst(self, dst, start, len):
		asdMinor = minor("/dev/%s" % self.name);
		cmd = system("echo r%d:%d:%d > /proc/asd/%s/%s/asdinfo" % ( 
					   asdMinor, start, len, self.pool.name, dst.name));
		return cmd;

	def unmap(self,block):
		cmdRet = system("asdunmap -b %d %s" % (block,self.name));
		return cmdRet;
	
	def unmap_proc(self,start,count):
		cmdRet = system("echo u%d:%d:1 > /proc/asd/%s/%s/asdinfo" % (start,count,self.name,self.pool));
		return cmdRet;

	def dumpMap(self):
		fd = open(self.path);
		assert fd;
		system("echo f%d >/proc/asd/sysinfo" % self.minor());
		fd.close();
		fd = open("/tmp/asdmap%d" % self.minor());
		str = fd.read();
		fd.close();
		return str;
	#prop related
	def setProp(self, start, count, prop):
		cmdRet = system("asd_prop_test --opcode 0 --blkstart %d --count %d --prop %s --device %s" 
			% (start, count, prop, self.path));
		return cmdRet;

	def setPropD(self, start, count):
		cmdRet = self.setProp(start, count, "D");
		return cmdRet;

	def setPropC(self, start, count):
		cmdRet = self.setProp(start, count, "C");
		return cmdRet;

	def setPropU(self, start, count):
		for (s, e) in eachSmallRange(start, start + count, 1024):
			cmdRet = self.setProp(s, e - s, "U");
			if (cmdRet.exitcode != 0):
				break;
		return cmdRet;
      
	def setPropR(self, dest_asd, start, count):
		asdMinor = minor("/dev/%s" % dest_asd.name);
		for (s,e) in eachSmallRange(start, start + count, 1024):
			cmdRet = system("asd_prop_test --opcode 0 --blkstart %d --count %d --prop R --device %s -t %d"
				% (start, count, self.path, asdMinor));
			if (cmdRet.exitcode != 0):
				break;
		return cmdRet;

	def getProp(self, start, count):
		cmdRet = system("asd_prop_test --opcode 1 --blkstart %d --count %d --device %s" % (start, count, self.path));
		return cmdRet;
	
	def clearBlocksIfError(self, start, count):
		ret = 0;
		stub.stop();
		cmd0 = self.getSetBlks(start, count); 
		self.clearSetBlks(start, count); 
		for (blk, result) in self.getSetBlks__blockResultPairs(cmd0):
			if result != 0:
				ret = result;
		stub.resume();
		return ret;

	def getProp__blockAttributePairs(self, cmd):
		if cmd.exitcode == 0:
			str = cmd.stdout;
			strList = str.split("\n")[6:-1];
			for i in strList:
				pair = i.split(", ");
				yield int(pair[0]), int(pair[1]);

	def getProp__assert(self, cmd, prop):
		assert cmd.exitcode == 0, (ASSERTION_FAILED + '''asd.getProp''');
		for (blk, attr) in self.getProp__blockAttributePairs(cmd):
			assert attr == prop, (ASSERTION_FAILED +
					"getProp:blk:%d:real-attr:%d:expected-attr:%d" % (blk, attr, prop));

	def getValidBlockProp(self, start, count):
		cmdRet = system("asd_prop_test --opcode 2 --blkstart %d --count %d --device %s" % (start, count, self.path));
		return cmdRet;

	def getValidBlockProp__blockAttributePairs(self, cmd):
		if cmd.exitcode == 0:
			str = cmd.stdout;
			strList = str.split("\n")[6:-1];
			for i in strList:
				pair = i.split(", ");
				yield int(pair[0]), int(pair[1]);

	def _hasMapOn(self, start, count):
		ret = False;
		cmd = self.getValidBlockProp(start, 1);
		for (blk, attr) in self.getValidBlockProp__blockAttributePairs(cmd):
			if blk >= start and blk < start + count:
				ret = True;
				break;
		return ret;

	def hasMapOn(self, start, count):
		stub.stop();
		ret = self._hasMapOn(start, count);
		stub.resume();
		return ret;

	def assert_hasMapOn(self, start, count):
		assert self._hasMapOn(start, count), (
			   ASSERTION_FAILED + "%s _hasMapOn range [%d, %d)" % (
							   self.name, start, start + count));

	def assert_hasNoMapOn(self, start, count):
		assert not self._hasMapOn(start, count), (
			   ASSERTION_FAILED + "%s _hasNoMapOn range [%d, %d)" % (
							   self.name, start, start + count));

	def getSetBlks(self, start, count):
		cmdRet = system("asd_prop_test --opcode 3 --blkstart %d --count %d --device %s" % (start, count, self.path));
		return cmdRet;

	def getSetBlks__blockResultPairs(self, cmd):
		assert cmd.exitcode == 0
		str = cmd.stdout;
		strList = str.split("\n")[6:-1];
		for i in strList:
			pair = i.split(", ");
			yield int(pair[0]), int(pair[1]);

	def clearSetBlks(self, start, count):
		for (s, e) in eachSmallRange(start, count + start, 1024):
			cmdRet = system("asd_prop_test --opcode 4 --blkstart %d --count %d --device %s" % (s, e - s, self.path));
		return cmdRet;

	def testSetBlks(self, start, count):
		cmdRet = system("asd_prop_test --opcode 5 --blkstart %d --count %d --device %s" % (start, count, self.path));
		return cmdRet;

	def testSetBlks__blockResultPairs(self, cmd):
		if cmd.exitcode == 0:
			str = cmd.stdout;
			strList = str.split("\n")[6:-1];
			for i in strList:
				pair = i.split(", ");
				yield int(pair[0]), int(pair[1]);
	

class AsdPool(PoolCheck):
	def __init__(self, name, granul, *phydevs):
		PoolCheck.__init__(self, name);
		self.name = name
		self.granul = granul
		self.phydevs = []
		self.asds = []
		self.appendPhyDev(phydevs);

	def __del__(self):
		pass;
	#	self.phydevs.clear();
	#	self.asds.clear();

	def appendPhyDev(self, phydevs):
		for i in phydevs:
			self.phydevs.append(i);

	def eachPhyDevPath(self):
		for i in self.phydevs:
			yield i.path;

	def remove(self):
		return system("asdpoolremove -f %s" % self.name);

	def display(self):
		cmd = "asdpooldisplay -n %s" % self.name
		return system(cmd);

	def displayDetail(self):
		cmd = "asdpooldisplay -l -p -n %s" % self.name
		return system(cmd);

	def setInactive(self):
		cmd = "asdpoolchange -a n %s" % self.name
		return system(cmd);

	def setActive(self):
		cmd = "asdpoolchange -a y %s" % self.name
		return system(cmd);

	def getAvailableSize(self):
		cmd = "asdpooldisplay -n %s -c" % self.name;
		available_size = system(cmd).stdout.split(":")[9];
		return atoi(available_size);

	def createAsd(self, asd):
		cmd = "asdcreate -n %s -L %s %s" % (asd.name, asd.size, self.name);
		print cmd;
		cmdRet = system(cmd);
		if (cmdRet.exitcode == 0):
			self.asds.append(asd);
		return cmdRet;
	
	def createAsds(self, asd_num, size):
		for x in xrange(asd_num):
			cmd = "asdcreate -n asd%d -L %dG %s" % (x, size, self.name);
			cmdRet = system(cmd);
			if (cmdRet.exitcode == 0):
				self.asds.append(asd);
			return cmdRet;

	def removeAsds(self):
		cmdRet = None;
		for asd in self.asds:
			cmdRet = asd.setInactive();
			if (cmdRet.exitcode == 0):
				cmdRet = asd.remove();
				if cmdRet.exitcode != 0:
					break;
			else:
				break;
		return cmdRet;

	def popen_ls_proc(self):
		cmd = "ls /proc/asd/%s/" % self.name;
		return system(cmd).stdout;

class _AsdSys(SysCheck):
	def __init__(self):
		SysCheck.__init__(self);
		self.pools = [];
		self.displayResult = [];
	
	def __del__(self):
		pass;
	#	self.pools.clear();
	#	self.displayResult.clear();
	
	#get asd sys info
	def display(self):
		cmd = "asdsysdisplay";
		cmdRet = system(cmd);
		return cmdRet;

	def displayInColonForm(self):
		cmd = "asdsysdisplay -c";
		cmdRet = system(cmd);
		return cmdRet;

	def updateDisplayResult(self):
		cmdRet = self.displayInColonForm();
		self.displayResult = cmdRet.stdout().split(":");

	def physicalDeviceCount(self):
		return int(self.displayResult[5]);

	def poolCount(self):
		return int(self.displayResult[2]);

	def asdDeviceCount(self):
		return int(self.displayResult[3]);

	def updatePdm(self):
		cmd = system("asd_update_pdm");
		return cmd;

	def pipe_proc_ls(self):
		cmd = "ls /proc/asd"
		return system(cmd).stdout;

	def createPool(self, pool):
		phyPaths = "";
		for i in pool.eachPhyDevPath():
			phyPaths = "%s %s" % (phyPaths, i)
		cmdRet = system("asdpoolcreate -n %s -g %d %s" %
				(pool.name, pool.granul, phyPaths));
		if cmdRet.exitcode == 0:
			self.pools.append(pool);
		return cmdRet;
	
	def removePools(self):
		cmdRet = None;
		for pool in self.pools:
			cmdRet = pool.setInactive();
			if cmdRet.exitcode == 0:
				cmdRet = pool.remove();
				if cmdRet.exitcode != 0:
					break;
			else:
				break;
		return cmdRet;
	
	#load/unload modules
	def load(self):
		self.updatePdm();
		self.loadPropTestModule();
		cmdRet = system("asd_load");
		if cmdRet.exitcode != 0:
			return cmdRet;
		cmdRet = system("modprobe asd_map_module");
		return cmdRet;

	def unload(self):
		system("modprobe -r asd_map_module");
		system("modprobe -r asd_driver");
		system("modprobe -r bwraidsched");
		cmdRet = system("modprobe -r bwraidpv");
		self.unloadPropTestModule();
		return cmdRet;

	def reload(self):
		cmd = self.unload();
		if (cmd.exitcode == 0):
			return self.load();
		
	def loadPropTestModule(self):
		cmdRet = system("modprobe asd_prop_test");
		return cmdRet;

	def unloadPropTestModule(self):
		cmdRet = system("modprobe -r asd_prop_test");
		return cmdRet;

	def tryUnload(self):
		print "-------- Try unload asd, it's not a part of test [begin] --------"
		self.unload();
		print "-------- Try unload asd, it's not a part of test [end] --------"

AsdSys = _AsdSys();

class _Stub:
	def __init__(self):
		self.maxTimes = 100;

	def unload(self):
		cmd = system("modprobe -r sm_stub");
		return cmd;

	def load(self):
		cmd = system("modprobe sm_stub");
		self.stop();
		return cmd;

	def start(self):
		cmd = system("echo I > /proc/sm_stub/stub");
		return cmd;

	def stop(self):
		cmd = system("echo F > /proc/sm_stub/stub");
		return cmd;

	def resume(self):
		cmd = system("echo i > /proc/sm_stub/stub");
		return cmd;

	def casesTriedUntilSuccess(self):
		global lastCmdExitcode;
		self.start();
		for i in xrange(0, self.maxTimes):
			os.system("echo \">>>>case tried until success:%d begin\">/dev/ttyS0" %i);
			yield i;
			os.system("echo \"<<<<case tried until success:%d end\">/dev/ttyS0" %i);
			if lastCmdExitcode == 0:
				break;
		self.stop();

stub = _Stub();

class Conf:
    def __init__(self, gran):
        self.gran = gran
        self.bs = 1<<gran
        self.stsize = conf_dict[gran]###
 
    def get_gran(self):
        return self.gran
 
    def get_bs(self):
        return self.bs
 
    def get_subtree_start(self, stid):
        return self.stsize * stid
 
    def get_subtree_size(self):
        return self.stsize


