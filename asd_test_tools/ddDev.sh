#!/bin/sh 

awk '$0 !~ /^#/' global_dd.info | awk '$0 !~ /^$/' | xargs ./_ddDev.py
