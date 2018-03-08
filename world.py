

class World():
    def __init__(self):
        self.worldInfo = {}

    # Calculate the subsection of the world visible to a specific agent.
    def _calculateFilteredInfo(self, agentID):
        filteredInfo = None
        return filteredInfo

    # Return information about the world.
    def getWorldInfo(self, agentID=None):
        if agentID is None:
            return self.worldInfo
        else:
            return self._calculateFilteredInfo(agentID)

    # Update the world state.
    def update(self, carPositions):
        self.worldInfo['carPositions'] = carPositions
