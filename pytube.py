#!/usr/bin/python

import sys
import os
import subprocess as sub
from time import sleep

urls = []
fp = open(sys.argv[1])
while 1:
    line = fp.readline()
    if line not in ["\n", ""]:
    	urls.append(l)
    if not line:
        break
for url  in urls:
	cmd = "youtube-dl "+x
	print cmd
	os.system(cmd)*
	sleep(300)

