import sys
import socket
import getopt
import threading
import subprocess as sub

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def how_to_use():
    print ""
    print "\t#####################"
    print "\t### myNetcat Tool ###"
    print "\t#####################"
    print "\tUsage: netcat.py -t target_host -p port"
    print "\t-l --listen 					- listen on [host]:[port] for incoming connection"
    print "\t-e --execute=file_to_run 	- execute the given file once receiving a connection"
    print "\t-c --command 				- initialize a command shell"
    print "\t-u --upload=destination      - once receiving connection, upload file and write to [destination]"
    print "\tExamples:"
    print "\tnetcat.py -t 192.168.1.1 -p 5000 -l -c"
    print "\tnetcat.py -t 192.168.1.1 -p 5000 -l -u=$HOME"
    print "\tnetcat.py -t 192.168.1.1 -p 5000 -l -e=\"echo $SHELL\""
    print "\techo 'message' | ./netcat.py -t 192.168.1.2 -p 6000"
    print ""
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)
        while(True):
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(8192)
                recv_len = len(data)
                response+=data
                if recv_len < 8192:
                    break
            print response,

            buffer = raw_input("")
            buffer+= "\n"
            client.send(buffer)
    except:
        print "[*] Exception ! sth went wrong!"
        client.close()

def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    while (True):
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()
    try:
        output = sub.check_output(command, stderr=sub.STDOUT, shell=True)
    except:
        output = "FAILED TO EXECUTE COMMAND.\r\n"
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command
    if len(upload_destination):
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer+= data

        try:
            fp = open(upload_destination, "wb")
            fp.write(file_buffer)
            fp.close()
            client_socket.send("Succesfully savec file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send("<HNACH:#> ")
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            response = run_command(cmd_buffer)
            client_socket.send(response)


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

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
    if listen:
        server_loop()

main()