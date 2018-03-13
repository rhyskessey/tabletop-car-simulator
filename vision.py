import server
import json
from time import time
from zenwheels.cars import MAC_TO_ID

class Vision():
    def __init__(self):
        s = server.Server()

    # Return the ID, pixel coordinates and orientation of every ZenWheels car.
    def locateCars(self):
        visionData = parse_json(server.latest_message)
        if visionData == None:
            return []
        if visionData['time']/1000 + 1 < time(): # Data is older than one second - discard.
            return []

        print(visionData)

        car_locations = []
        for mac_address in MAC_TO_ID:
            if mac_address in visionData:
                agentID = MAC_TO_ID[mac_address]
                pos = (visionData[mac_address][1], visionData[mac_address][2])
                angle = visionData[mac_address][5]
                observed_car = {'ID': agentID, 'position': pos, 'orientation': angle}
                car_locations.append(observed_car)
        return car_locations


def parse_json(msg):
    try:
        dict = json.loads(msg)
        return dict
    except:
        return None