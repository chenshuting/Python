#!/bin/sh 

awk '$0 !~ /^#/' global_phydev.info | awk '$0 !~ /^$/' | xargs ./_clearPhydev.py
