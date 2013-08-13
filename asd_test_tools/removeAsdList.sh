#!/bin/sh 

awk '$0 !~ /^#/' global_asdList.info | awk '$0 !~ /^$/' | xargs ./_removeAsd.py
