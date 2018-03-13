import pygame
from pygame.locals import *

DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 900
BACKGROUND_IMAGE_PATH = "media/map_image.jpg"

class Display():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))#, pygame.FULLSCREEN)
        self.background_image = self.loadBackground()

    # Load and scale background image.
    def loadBackground(self):
        background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        scale_factor = DISPLAY_WIDTH / background_image.get_rect().size[0]
        background_image = pygame.transform.rotozoom(background_image, 0, scale_factor)
        return background_image

    # Create image from raw world data.
    def createImage(self, worldData):
        self.screen.blit(self.background_image, (0,0))
        for vehicle in worldData['vehicles']:
            try:
                pos = (vehicle.position[0], DISPLAY_HEIGHT - vehicle.position[1])
                angle = vehicle.orientation
                width, length = vehicle.dimensions
                template = pygame.Surface((width,length))
                template.fill((255,255,255))
                template.set_colorkey((255,0,0))
                img = pygame.transform.rotate(template, angle)
                img_rect = img.get_rect(center=pos)
                self.screen.blit(img, img_rect)
            except:
                pass
                #print("ERROR: Could not display vehicle owned by Agent " + str(vehicle.owner.ID) + ".")

    # Update the world display.
    def update(self, worldData):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
        self.createImage(worldData)
        pygame.display.flip()

