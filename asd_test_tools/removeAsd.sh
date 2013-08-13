#!/bin/sh 

awk '$0 !~ /^#/' global_asd.info | awk '$0 !~ /^$/' | xargs ./_removeAsd.py
