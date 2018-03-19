import select
import threading
import time

from bluetooth import *

from zenwheels.cars import ID_TO_MAC

msgHeader = "[CAR COMMS]: "

BT_LOOP_SLEEP = 25

class CarCommunicator():
    def __init__(self, vehicles):
        self.known_vehicles = vehicles
        self.car_sockets = {}
        if self.connectToCars():
            self.startCarComms()
        else:
            print("Exiting.")
            exit()

    def connectToCars(self):
        print(msgHeader + "Connecting to the ZenWheels cars...")
        for car in self.known_vehicles:
            agent_id = car.owner.ID
            # Try to connect to each car three times
            connected = False
            for attempt in range(1,4):
                try:
                    print(msgHeader + "Connecting to %s (Attempt %d)." % (agent_id, attempt))
                    socket = BluetoothSocket(RFCOMM)
                    socket.connect((ID_TO_MAC[agent_id], 1))
                    self.car_sockets[agent_id] = socket
                    print(msgHeader + "Connected to %s." % agent_id)
                    connected = True
                    break
                except (BluetoothError, OSError) as e:
                    print(msgHeader + "Could not connect to %s because %s." % (agent_id, e))
            if connected == False:
                print(msgHeader + "All connection attempts to %s failed." % (agent_id))
                return False
        return True

    def startCarComms(self):
        t_process = threading.Thread(target=self.bt_send)
        t_process.daemon = True
        t_process.start()

    def bt_send(self):
        while True:
            for car in self.known_vehicles:
                socket = self.car_sockets[car.owner.ID]
                try:
                    can_read, can_write, has_error = select.select([], [socket], [], 0)
                    if socket in can_write:
                        try:
                            if not car.command_queue:
                                continue
                            command = car.command_queue.popitem()
                            # Send command
                            #print(msgHeader + "Sending command: " + str(command[0]))
                            socket.send(command[0])
                            # Calculate and print total system delay
                            #millis = int(round(time.time()*1000))
                            #print(msgHeader + "System Delay: %d ms" % (millis - command[1]))
                        except Exception as e:
                            print(msgHeader + str(e))
                            pass
                except (BluetoothError, OSError, ValueError) as e:
                    print(msgHeader + str(e))
                    socket.close()

            # Ray: Sleep is essential otherwise all system resources are taken and total system delay skyrockets.
            time.sleep(BT_LOOP_SLEEP / 1000)
