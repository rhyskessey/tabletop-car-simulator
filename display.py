import pygame

DISPLAY_WIDTH = None
DISPLAY_HEIGHT = None
BACKGROUND_IMAGE_PATH = None

class Display():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
        self.background_image = self.loadBackground()

    # Load and scale background image.
    def loadBackground(self):
        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        scale_factor = DISPLAY_WIDTH / background_image.get_rect().size[0]
        background_image = pygame.transform.rotozoom(background_image, 0, scale_factor)
        return background_image

    # Create png image from raw world data.
    def createImage(self, worldInfo):
        image = self.background_image
        return image

    # Update the world display.
    def update(self, worldInfo):
        image = self.createImage(worldInfo)
        self.screen.blit(image)