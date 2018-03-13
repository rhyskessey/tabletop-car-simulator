import socket
import threading
import socketserver

HOST = "localhost"
PORT = 1520

latest_message = None # TODO: Find a better way of grabbing messages from the request handler.

class Server():
    def __init__(self):
        self.server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global latest_message
        while True:
            try:
                data = self.request.recv(1024)
                if data == None or data == b'':
                    break
                latest_message = data.decode('utf-8')
            except:
                break

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# For testing.
def fake_client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(1024)
        print("Received: {}".format(response))
    finally:
        sock.close()
