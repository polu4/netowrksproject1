'''
A simple TCP "echo" server written in Python.

author:  Amy Csizmar Dalal and [YOUR NAMES HERE]
CS 331, Fall 2025

Minimal Gopher server (RFC-style behaviour for menus and text files).
It serves files from the ./content/directory and responds with either a menu (directory listing) or a text file
Menu and text responses are terminated with a single period
To test, use the default port `localhost 48999`.
'''
import sys, socket
DEFAULT_PORT = 48999

# Server logic
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
            # Get the message and respond
            while True:
                data = clientSock.recv(1024)
                if not data:
                    break # client closed connection
                
                selector = data.decode("ascii").strip()
                print(f"Received selector: '{selector}'")

                if selector == "" or selector == "\\r\\n":
                    resource_path = "content/links.txt"
                else:
                    if ".." in selector:
                        error_msg = b"3Invalid selector.\terror\terror\r\n"
                        clientSock.sendall(error_msg)
                        break
                    resource_path = "content/" + selector

                try:
                    with open(resource_path, "rb") as f:
                        response = (f.read()).decode("ascii")
                        response += "\n."
                        response = response.encode("ascii")
                    clientSock.sendall(response)
                except FileNotFoundError:
                    print(f"File not found: {resource_path}")
                    error_msg = f"3'{selector}' not found.\terror\terror\r\n".encode("ascii")
                    clientSock.sendall(error_msg)
                
                # We've sent our response, so break this inner loop
                break
            clientSock.close()

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