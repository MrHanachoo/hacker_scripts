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
    	urls.append(line)
    if not line:
        break
for url  in urls:
	cmd = "youtube-dl "+url
	print cmd
	os.system(cmd)
	#sleep(60)

