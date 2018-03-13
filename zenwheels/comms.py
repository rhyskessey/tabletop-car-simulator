import time
import threading
from bluetooth import *
import select
from collections import deque
from zenwheels.cars import ID_TO_MAC

BT_LOOP_SLEEP = 25

class CarCommunicator():
    def __init__(self):
        self.car_sockets = {}
        self.command_queue = deque()
        if self.connectToCars():
            self.startCarComms()

    def connectToCars(self, active_agents):
        # Try connect to all of our cars
        print("Connecting to the ZenWheels cars...")
        for agent_id in ID_TO_MAC:
            # Try to connect to each car three times
            for x in range(1,4):
                try:
                    print("Connecting to %s (Attempt %d)" % (agent_id, x))
                    socket = BluetoothSocket(RFCOMM)
                    socket.connect((ID_TO_MAC[agent_id], 1))
                    self.car_sockets[agent_id] = socket
                    print("Connected to %s" % agent_id)
                    break
                except (BluetoothError, OSError) as e:
                    print("Could not connect to %s because %s" % (agent_id, e))
                    return False
        return True


    def startCarComms(self):
        t_process = threading.Thread(target=self.bt_send)
        t_process.daemon = True
        t_process.start()

    def bt_send(self):
        for _, socket in car_sockets.items():
            try:
                can_read, can_write, has_error = select.select([], [socket], [], 0)
                if socket in can_write:
                    try:
                        item = vehicle.out_dict.popitem()
                    except KeyError:
                        # Dictionary is empty, do nothing
                        pass
                    else:
                        # Send command
                        vehicle.socket.send(item[0])

                        # Calculate and print total system delay
                        millis = int(round(time.time() * 1000))
                        print("System Delay: %d ms" % (millis - item[1]))

                        # TODO log delays to file for analysis

            except (BluetoothError, OSError, ValueError) as e:
                print(e)
                vehicle.socket.close()
                common.vehicle.remove(vehicle)

        # Sleep is essential otherwise all system resources are taken and total system delay skyrockets
        time.sleep(BT_LOOP_SLEEP / 1000);