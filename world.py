from agent import Agent

class World():
    def __init__(self, agentIDs):
        # Initialise agents and their vehicles.
        agents = []
        vehicles = []
        for agentID in range(agentIDs):
            agent = Agent(agentID)
            agents.append(agent)
            vehicles.append(agent.vehicle)
        self.worldData = {'agents': agents, 'vehicles': vehicles}

    # Update the world state.
    def update(self, car_locations):
        for observed_car in car_locations:
            for known_vehicle in self.worldData['vehicles']:
                if int(observed_car['ID']) == known_vehicle.owner.ID:
                    known_vehicle.position = observed_car['position']
                    known_vehicle.orientation = observed_car['orientation']

    def getWorldData(self):
        return self.worldData