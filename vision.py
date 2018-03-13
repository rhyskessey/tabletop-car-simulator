
import socketserver
import threading

class Vision():
    def __init__(self):
        print("VISION: Start server...")
        t = ThreadedTCPServer(('localhost', 1520), Service)
        server_thread = threading.Thread(target=t.serve_forever())
        server_thread.daemon = True
        server_thread.start()

    # Return the ID, pixel coordinates and orientation of every ZenWheels car.
    def locateCars(self):
        car_locations = []
        return car_locations


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class Service(socketserver.BaseRequestHandler):
    def handle(self):
        while 1:
            self.data = self.request.recv(1024)

            print("Data: ", self.data)

            print('Handling request')
            if not (self.data):
                print("No data received.")
                break

        self.request.close()