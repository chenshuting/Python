#!/bin/sh 

DIR=`pwd`;
cd $DIR;

if [ $# -eq 0 ];then
	echo "Usage:$0 type[0:update code; 1:update tags]";
	exit;
fi

if [ $1 -eq 0 ];then
	svn up;
fi

if [ $1 -eq 1 ];then
	ctags -R;
	cscope -Rbqk;
fi
