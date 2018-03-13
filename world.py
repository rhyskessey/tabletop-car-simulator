import agent

class World():
    def __init__(self, numAgents):
        # Initialise agents and their vehicles.
        agents = []
        vehicles = []
        for i in range(numAgents):
            agents.append(agent.Agent(i))
            vehicles.append(agents[i].vehicle)
        self.worldData = {'agents': agents, 'vehicles': vehicles}

    # Update the world state.
    def update(self, car_locations):
        for observed_car in car_locations:
            for known_vehicle in self.worldData['vehicles']:
                if observed_car['ID'] == known_vehicle.owner.ID:
                    known_vehicle.position = observed_car['position']
                    known_vehicle.orientation = observed_car['orientation']

    def getWorldData(self):
        return self.worldData