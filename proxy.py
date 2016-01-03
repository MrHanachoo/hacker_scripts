__author__ = 'med'

import sys
import socket
import threading


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print bcolors.FAIL+ "[x] Failed to listen on %s:%d" % (local_host, local_port) + bcolors.ENDC
        print bcolors.BOLD+ "[i] Check for another listening sockets or correct permissions."+ bcolors.ENDC
        sys.exit(0)

    print bcolors.OKGREEN+ "[*] Listening on %s:%d" % (local_host, local_port)+ bcolors.ENDC
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print client_socket
        print bcolors.OKGREEN+"[=>] Received incoming connection from %s:%d" % (addr[0], addr[1]) + bcolors.ENDC

        # start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # let's connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from remote if necessary
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # if we have data to send to our local client, send it
        if len(remote_buffer):
            print bcolors.OKBLUE+ "[<==] Sending %d bytes to localhost." % len(remote_buffer)+ bcolors.ENDC
            client_socket.send(remote_buffer)

    # now let's loop and read from local, send to remote, send to local
    # rinse, wash, repeat
    while True:
        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print bcolors.OKBLUE+ "[==>] Received %d bytes from localhost." % len(local_buffer)+ bcolors.ENDC
            hexdump(local_buffer)

            # send it to our request handler
            local_buffer = request_handler(local_buffer)

            # send off data to the remote host
            remote_socket.send(local_buffer)
            print bcolors.OKGREEN+ "[==>] Sent to remote."+ bcolors.ENDC

        # receive back the response
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print bcolors.OKGREEN+ "[<==] Received %s bytes from remote." % len(remote_buffer)+ bcolors.ENDC
            hexdump(remote_buffer)

            # send to our response handler
            remote_buffer = response_handler(remote_buffer)

            # send the response to the local socket
            client_socket.send(remote_buffer)

            print bcolors.OKBLUE+ "[<==] Sent to localhost."+ bcolors.ENDC

        # if no more data to either side, close the connections
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print bcolors.WARNING+ "[*] No more data. "+bcolors.ENDC + bcolors.FAIL+ "Closing connections"+ bcolors.ENDC

            break


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%04X %-*s %s" % (i, length*(digits + 1), hexa, text))

    print b'\n'.join(result)


def receive_from(connection):
    buffer = ""
    # the timeout is setted to 2 sec
    connection.settimeout(10)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer+= data
    except:
        pass
    return buffer


def request_handler(buffer):
    return buffer


def response_handler(buffer):
    return buffer


def main():
    # command line control
    if len(sys.argv[1:]) !=5:
        print bcolors.FAIL+ "Usage: python proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"+ bcolors.ENDC
        print bcolors.OKGREEN+ "Example: python proxy.py localhost 8000 192.168.1.100 8000 True"+ bcolors.ENDC
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remot_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # this tells our proxy to connect and receive data before sending to remote host
    receive_first = sys.argv[5]
    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # let's spin up our listening socket
    server_loop(local_host, local_port, remot_host, remote_port, receive_first)

main()
