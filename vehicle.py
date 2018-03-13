

class Vehicle:
    owner = None
    position = None, None   # World coordinates (x, y).
    orientation = None      # Degrees clockwise from north.
    dimensions = None, None # Size and shape (width, length).
    max_speed = None
    max_acceleration = None
    max_deceleration = None
    max_turn = None
    max_turn_change = None

    def __init__(self, owner):
        self.owner = owner


class Car(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 50
        self.dimensions = (35,60)

class Truck(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 40
        self.dimensions = (40,90)

class Motorcycle(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 60
        self.dimensions = (15,30)

class Bicycle(Vehicle):
    def __init__(self, owner):
        Vehicle.__init__(self, owner)
        self.max_speed = 20
        self.dimensions = (8,25)


if __name__ == "__main__":
    vehicles = [Car(), Truck(), Motorcycle(), Bicycle()]
    for vehicle in vehicles:
        vehicle.getInfo()
