#!/bin/sh 

awk '$0 !~ /^#/' global_pool.info | awk '$0 !~ /^$/' | xargs ./_createPool.py
