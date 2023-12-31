#turrets.py
import pygame
import constants as c

class Turret(pygame.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y, initial_size=(c.TILE_SIZE,c.TILE_SIZE)):
        pygame.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y

        #calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE
        self.original_image = image
        self.image = pygame.transform.scale(self.original_image, initial_size)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
