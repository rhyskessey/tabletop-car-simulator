import json
from time import time
from zenwheels.cars import MAC_TO_ID
import socket
import threading
import socketserver

msgHeader = "[VISION]: "

HOST = "localhost"
PORT = 1520

latest_message = None # TODO: Find a better way of grabbing messages from the request handler.

class Vision():
    def __init__(self):
        s = Server()
        print(msgHeader + "Initialisation complete.")

    # TODO: The C++ script gives a weird orientation value - find a way to compensate.
    # Return the ID, pixel coordinates and orientation of every ZenWheels car.
    def locateCars(self):
        visionData = parse_json(latest_message)
        if visionData == None:
            return []
        if visionData['time']/1000 + 1 < time(): # Data is older than one second - discard.
            return []
        car_locations = []
        for mac_address in MAC_TO_ID:
            if mac_address in visionData:
                agentID = MAC_TO_ID[mac_address]
                pos = (visionData[mac_address][1], visionData[mac_address][2])
                angle = visionData[mac_address][5]
                observed_car = {'ID': agentID, 'position': pos, 'orientation': angle}
                car_locations.append(observed_car)
        return car_locations

class Server():
    def __init__(self):
        self.server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(msgHeader + "Server loop running in thread:", server_thread.name)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global latest_message
        print(msgHeader + "Received connection from " + str(self.client_address[0]) + ".")
        while True:
            try:
                data = self.request.recv(1024)
                if data == None or data == b'':
                    break
                latest_message = data.decode('utf-8')
            except:
                print(msgHeader + "Client " + str(self.client_address[0]) + " disconnected.")
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

def parse_json(msg):
    try:
        dict = json.loads(msg)
        return dict
    except:
        return None