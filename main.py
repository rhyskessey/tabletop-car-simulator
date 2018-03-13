import world, vision, display

NUM_AGENTS = 2

if __name__ == "__main__":
    # System initialisation.
    vision = vision.Vision()
    display = display.Display()
    world = world.World(NUM_AGENTS)

    # Event loop.
    while True:
        car_locations = vision.locateCars()
        world.update(car_locations)
        display.update(world.getWorldData())
        print("loop")