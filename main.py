from world import World
from vision import Vision
from display import Display
from zenwheels.comms import CarCommunicator

ACTIVE_AGENTS = [45, 10]

if __name__ == "__main__":
    # System initialisation.
    vision = Vision()
    display = Display()
    world = World(ACTIVE_AGENTS)
    comms = CarCommunicator()

    # Event loop.
    while True:
        car_locations = vision.locateCars()
        world.update(car_locations)
        display.update(world.getWorldData())
