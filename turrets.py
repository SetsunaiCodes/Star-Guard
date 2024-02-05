#|| turrets.py ||
import pygame
import math
import constants as c
from turret_data import TURRET_DATA 

class Turret(pygame.sprite.Sprite):
    def __init__(self, turret_type, sprite_sheet, tile_x, tile_y):
        pygame.sprite.Sprite.__init__(self)
        self.range = TURRET_DATA.get(turret_type)["range"]
        self.cooldown = TURRET_DATA.get(turret_type)["attack_cooldown"]
        self.last_shot = pygame.time.get_ticks()
        self.selected = False
        self.target = None
        self.tile_x = tile_x
        self.tile_y = tile_y

        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        #Startwinkel
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]

        #entsprechende Drehung
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.range_image = pygame.Surface((self.range *2, self.range *2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pygame.draw.circle(self.range_image, "grey100",(self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    # Einladen aller Sprites und dann in einer Liste speichern
    def load_images(self):
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            temp_img_scaled = pygame.transform.scale(temp_img, (c.TILE_SIZE,c.TILE_SIZE))
            animation_list.append(temp_img_scaled)
        return animation_list
    
    # Sprites aktualisieren 
    def update(self,enemy_group):
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            self.play_animation()
            self.pick_target(enemy_group)


    # Ziel definieren
    def pick_target(self,enemy_group):

        x_dist = 0
        y_dist = 0

        #Distanz zu jedem (sich aktuell auf dem Feld befindenden) Gegner überprüen
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    #Drehung, wenn das Ziel gefunden wurde
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    #damage
                    self.target.health -= c.DAMAGE
                    break

    # Animationsliste durchlaufen
    def play_animation(self):
        self.original_image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            self.last_shot = pygame.time.get_ticks()
        
    # Turret anzeigen
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle -90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)


    
