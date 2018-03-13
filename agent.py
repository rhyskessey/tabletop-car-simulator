import vehicle

class Agent():
    def __init__(self, ID, vehicleType=vehicle.Car):
        self.ID = ID
        self.vehicle = vehicleType(self)
        self.worldKnowledge = {'waypoints': [], 'obstacles': []}

