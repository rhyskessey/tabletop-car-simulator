
msgHeader = "[WORLD]: "

class World():
    def __init__(self, agents, vehicles, waypoints=None):
        self.worldData = {'agents': agents, 'vehicles': vehicles, 'waypoints': waypoints}
        print(msgHeader + "Initialisation complete.")

    # Update the world state.
    def update(self, car_locations):
        for known_vehicle in self.worldData['vehicles']:
            updated = False
            for observed_car in car_locations:
                if observed_car['ID'] == known_vehicle.owner.ID:
                    known_vehicle.position = observed_car['position']
                    known_vehicle.orientation = observed_car['orientation']
                    updated = True
                    break
            if not updated:
                known_vehicle.position = (None, None)
                known_vehicle.orientation = None

    def getWorldData(self):
        return self.worldData