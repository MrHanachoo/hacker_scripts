#!/usr/bin/python

import sys
import os
import subprocess as sub

xx = []
fp = open(sys.argv[1])
while 1:
    l = fp.readline()
    if l not in ["\n", ""]:
    	xx.append(l)
    if not l:
        break
for x in xx:
	c = "youtube-dl "+x
	print c
	os.system(c)

