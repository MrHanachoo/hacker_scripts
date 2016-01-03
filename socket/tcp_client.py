import socket 
import sys

if not len(sys.argv) == 5:
    print "USAGE: python tcp_client.py [target_host] [target_port] [recv_port] [message]"
    sys.exit(1)

target_host = sys.argv[1]
target_port = int(sys.argv[2])
recv_port = int(sys.argv[3])
message = sys.argv[4]
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
client.send(message)

# receive some data
response = client.recv(recv_port)

print response