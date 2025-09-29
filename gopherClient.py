'''
A simple "echo" client written in Python.

author:  Amy Csizmar Dalal and Alden Harcourt, Sam Lengyel Luke Poley
CS 331, Fall 2025
'''
import sys, socket

def usage():
    print ("Usage:  python SimpleTCPClient <server IP> <port number> <message>")
    sys.exit()

def main():
    # Process command line args (server, port, message)
    if len(sys.argv) < 4:
        usage()

    try:
        server = sys.argv[1]
        port = int(sys.argv[2])
        message = sys.argv[3]
    except ValueError as e:
        usage()

    serverSock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSock.connect((server, port))
    print ("Connected to server; sending message")

    # Actually send the message; Both server and client encode and decode in ascii.
    serverSock.send(message.encode("ascii"))
    print ("Sent message; waiting for reply")

    returned = serverSock.recv(1024)

    # Defined Item-Type Character in Gopher for Files, Directories, Error Messages
    FILE = '0'
    DIRECTORY = '1'
    ERROR = '3'
    reply = returned.decode("ascii")
    if reply[0] == ERROR:
        # Special case if the user tries to use *Nix parent directory operator. May expand later to allow going up a level with this.
        if reply[1] == '.' and reply [2] == '.':
            print ("\"..\" not a valid selector string")
        # Otherwise tell the user that they just asked for an invalid file or directory.
        else:
            print ("ERROR - " + message + " not a valid file or directory")
    elif reply[0] == DIRECTORY:
        print ("Received reply: \n"+ reply)
    elif reply[0] == FILE:
        savePath = input("Enter the path to where you want to save " + message + " or press enter to save the file in your current directory") + message
        with open(resource_path, "wb") as downloadedFile:
            downloadedFile.write(reply)
        print(message + " downloaded to resource_path")

    serverSock.close()

main()
