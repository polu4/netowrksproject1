'''
A simple TCP "echo" server written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2025

Minimal Gopher server (RFC-style behaviour for menus and text files).
It serves files from the ./content/directory and responds with either a menu (directory listing) or a text file
Menu and text responses are terminated with a single period
To test, use the default port `localhost 48999`.
'''
import sys, socket, os
DEFAULT_PORT = 48999

# Defines the logic for our Gopher server.
class TCPServer:
    # Sets up the server socket
    def __init__(self, port=DEFAULT_PORT):
        self.port = port
        self.host = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    # Waits for connections and handles them.
    def listen(self):
        self.sock.listen(5)

        # Continues to accept new connections
        while True:
            clientSock, clientAddr = self.sock.accept()
            print ("Connection received from ",  clientSock.getpeername())
            while True:
                data = clientSock.recv(1024)
                if not data:
                    break # client closed connection
                
                selector = data.decode("ascii").strip()
                print(f"Received selector: '{selector}'")

                # Determine what client wants
                if selector == "" or selector == "\\r\\n":
                    # Client wants main menu.
                    resource_path = "content/links.txt"
                    try:
                        with open(resource_path, "rb") as f:
                            response = f.read()
                        clientSock.sendall(response)
                    except FileNotFoundError:
                        print(f"File not found: {resource_path}")
                        error_msg = f"3'links.txt' not found.\terror\terror\r\n".encode("ascii")
                        clientSock.sendall(error_msg)
                else:
                    # Determine resource type.
                    gopher_type = selector[0]
                    # The rest of the selector is the path.
                    path = selector[1:] 

                    # Security check to prevent accessing parent directories.
                    if ".." in path:
                        error_msg = b"3Invalid selector.\terror\terror\r\n"
                        clientSock.sendall(error_msg)
                        break
                    
                    resource_path = "content/" + path

                    try:
                        if gopher_type == '0':
                            # Type 0 is a file.
                            with open(resource_path, "rb") as f:
                                response = (f.read()).decode("ascii")
                                response += "\n."
                                response = response.encode("ascii")
                            clientSock.sendall(response)
                        elif gopher_type == '1':
                            # Type 1 is a directory.
                            menu_path = os.path.join(resource_path, "links.txt")
                            with open(menu_path, "rb") as f:
                                response = f.read()
                            clientSock.sendall(response)
                        else:
                            # Handle unknown types by treating them as not found.
                            raise FileNotFoundError

                    except FileNotFoundError:
                        print(f"Resource not found: {resource_path}")
                        error_msg = f"3'{selector}' not found.\terror\terror\r\n".encode("ascii")
                        clientSock.sendall(error_msg)
                
                break
            clientSock.close()

# Sets up and starts the server.
def main():
    if len(sys.argv) > 1:
        try:
            server = TCPServer(int(sys.argv[1]))
        except ValueError as e:
            print ("Error in specifying port. Creating server on default port.")
            server = TCPServer()
    else:
        server = TCPServer()

    # Listen forever
    print ("Listening on port " + str(server.port))
    server.listen()

main()