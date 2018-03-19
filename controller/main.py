from agent import Agent
from vision import Vision
from world import World
from display import Display
from zenwheels.cars import *
from zenwheels.comms import CarCommunicator


ACTIVE_CARS = [ORANGE_CAR_ID]

if __name__ == "__main__":
    print("")
    print("========================================")
    print("         TABLETOP CAR SIMULATOR         ")
    print("========================================")
    print("")

    # Initialise vision server.
    vision = Vision()

    # Initialise display.
    display = Display()

    # Initialise agents and their vehicles.
    agents = []
    vehicles = []
    for agentID in ACTIVE_CARS:
        agent = Agent(agentID, strategyFile="strategies/spazout.txt")
        agents.append(agent)
        vehicles.append(agent.vehicle)

    # Initialise world.
    world = World(agents, vehicles)

    # Initialise car communicator.
    comms = CarCommunicator(vehicles)

    # Event loop.
    while True:
        car_locations = vision.locateCars()
        world.update(car_locations)
        display.update(world.getWorldData())
        for agent in agents:
            agent.update_world_knowledge(world.getWorldData())
            agent.make_decision()
