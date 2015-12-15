__author__ = 'med'

import socket
import paramiko
import threading
import sys


host_key = paramiko.RSAKey(filename='/home/med/.ssh/id_rsa')


class Server(paramiko.ServerInterface):

    def __init__(self):
        self.event =threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'med') and (password == "passwd"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print '[+] Listening for connection ...'
    client, addr = sock.accept()
except Exception, e:
    print '[-] Listen failed: ' + str(e)
    sys.exit(1)
print '[+] Got a connection!'

try:
    mySession = paramiko.Transport(client)
    mySession.add_server_key(host_key)
    server = Server()
    try:
        mySession.start_server(server=server)
    except paramiko.SSHException, e:
        print '[!] SSH negotiation failed.'
    chan = mySession.accept(20)
    print '[*] Authenticated !'
    print chan.recv(1024)
    chan.send('Welcome to med_ssh')
    while True:
        try:
            command = raw_input("ENTER COMMAND: ").strip("\n")
            if command != 'exit':
                chan.send(command)
                print chan.recv(1024)+ "\n"
            else:
                chan.send("exit")
                print "exiting"
                mySession.close()
                raise Exception ("exit")
        except KeyboardInterrupt:
            mySession.close()
except Exception, e:
    print "[!] Caught exeception: "+ str(e)
    try:
        mySession.close()
    except:
        pass
    sys.exit(1)
