import vehicle

class Agent():
    def __init__(self, ID):
        self.ID = ID
        self.myVehicle = vehicle.Vehicle()

    # Update the agent's world knowledge.
    def update(self, worldInfo):
        self.worldInfo = worldInfo