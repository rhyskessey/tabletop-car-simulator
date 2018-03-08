import world, vision, display, agent

NUM_AGENTS = 4

if __name__ == "__main__":
    # System initialisation.
    world = world.World()
    vision = vision.Vision()
    display = display.Display()
    agents = []
    for i in range(NUM_AGENTS):
        agents.append(agent.Agent(i))

    # Event loop.
    while True:
        carPositions = vision.getCarPositions()
        world.update(carPositions)
        display.update(world.getWorldInfo())
        for agent in agents:
            agent.update(world.getWorldInfo(agentID=agent.ID))