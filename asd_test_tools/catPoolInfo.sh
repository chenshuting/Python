#!/bin/sh 

awk '$0 !~ /^#/' global_asd.info | awk '$0 !~ /^$/i {print $0}' | xargs cat /proc/asd/ap0/poolinfo
