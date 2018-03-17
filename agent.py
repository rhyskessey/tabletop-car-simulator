import vehicle

msgHeader = "[AGENT]: "

class Agent():
    def __init__(self, ID, agentType="robot", vehicleType=vehicle.Car, strategyFile=None):
        self.ID = str(ID)
        if agentType == "human":
            self.cone_of_vision = 120
        else:
            self.cone_of_vision = 360
        self.vehicle = vehicleType(self)
        self.worldKnowledge = {'waypoints': [],
                               'obstacles': []}
        self.strategy = None
        if strategyFile is not None:
            try:
                with open(strategyFile, "r") as f:
                    self.strategy = f.read()
                print(msgHeader + "Successfully loaded the strategy file for Agent " + self.ID + ".")
            except:
                print(msgHeader + "Could not open the strategy file for Agent " + self.ID + ".")

    def update_world_knowledge(self, worldData):
        # TODO: Work on this.
        for key in self.worldKnowledge:
            if key in worldData:
                self.worldKnowledge[key] = worldData[key]

    def make_decision(self):
        if self.strategy is not None:
            # TODO: Should probably find a more secure way to run custom agent scripts.
            exec(self.strategy)
        else:
            self.default_strategy()

    def default_strategy(self):
        pass