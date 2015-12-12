import sys
import socket
import getopt
import threading
import subprocess as sub

# let's define some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def how_to_use():
	print "myNetcat Tool\n"
	print "Usage: netcat.py -t target_host -p port"
	print "-l --listen 					- listen on [host]:[port] for incoming connection"
	print "-e --execute=file_to_run 	- execute the given file once receiving a connection"
	print "-c --command 				- initialize a command shell"
	print "-u --upload=destination      - once receiving connection, upload file and write to [destination]\n\n"
	print "Examples:"
	print "netcat.py -t 192.168.1.1 -p 5000 -l -c"
	print "netcat.py -t 192.168.1.1 -p 5000 -l -u=$HOME"
	print "netcat.py -t 192.168.1.1 -p 5000 -l -e=\"echo $SHELL\""
	print "echo 'message' | ./netcat.py -t 192.168.1.2 -p 6000"
	sys.exit(0)

def main():
	global listen
	global command
	global upload
	global execute
	global target
	global upload_destination
	global port

	if not len(sys.argv[1:]):
		how_to_use()

	# read the commendline option
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",
			["help", "listen", "execute", "target", "port", "command", "upload"])
	except getopt.GetoptError as e:
		print str(e)
		how_to_use()
	
	for x, y in opts:
		if x in ("-h", "--help"):
			how_to_use()
		elif x in ("-l", "--listen"):
			listen = True
		elif x in ("-e", "--execute"):
			execute = y
		elif x in ("-c", "--command_shell"):
			command = True
		elif x in ("-u", "--upload"):
			upload_destination = y
		elif x in ("-t", "--target"):
			target = y
		elif x in ("-p", "--port"):
			port = int(y)
		else:
			assert False, "Unhandled Option"