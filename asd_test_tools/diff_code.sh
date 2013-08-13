#!/bin/sh 

awk '$0 !~ /^#/' global_diff.info | awk '$0 !~ /^$/' | xargs ./_diff_code.py
