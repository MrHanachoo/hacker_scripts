import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

# create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))
server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip, bind_port)

# this is the client_handling thread
def client_handler_to_thread(client_socket):

	# received request
	request = client_socket.recv(1111)
	print "[*] Received: %s\n" % request

	#send back a packet 
	client_socket.send("ACK!")
	client_socket.close()

	
while True:
		
	client, addr = server.accept()
	print "[*] Accepted connection from %s:%d" % (addr[0], addr[1])
	#print client, addr

	# spin up the client thread
	client_handler = threading.Thread(target=client_handler_to_thread, args=(client,))
	client_handler.start() 