#maingame.py
import pygame
import json
from enemy import Enemy
from turrets import Turret
from world import World
import constants as c



#Initialisierung
pygame.init()

#Clock erstellen
clock = pygame.time.Clock()


#Fenstereinstellungen treffen
screen = pygame.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
pygame.display.set_caption("StarGuard")

#load images
#map
map_image = pygame.image.load('levels/map.png').convert_alpha()
#individual turret image for mouse cursor
cursor_turret = pygame.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
#enemy
enemy_image = pygame.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

#load json data for level
with open('levels/map.tmj') as file:
    world_data = json.load(file)

#World Gruppe
world = World(world_data, map_image)
world.process_data()

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE

    #calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    
    if world.tile_map[mouse_tile_num] != 11:
        #Check ob das Tile besetzt ist
        space_is_free = True
        for turret in turret_group:
            if(mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        #Wenn der Platz frei ist, dann setzen wir ein Turret
        if space_is_free == True:
            new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

#Enemy Gruppe
enemy_group = pygame.sprite.Group()
#Turret Gruppe
turret_group = pygame.sprite.Group()

enemy = Enemy(world.waypoints, enemy_image)
 #Gegner der Gruppe hinzufügen
enemy_group.add(enemy)


#game loop
run = True
while run:
    clock.tick(c.FPS)
    screen.fill("grey100")

    world.draw(screen)

    pygame.draw.lines(screen, "grey0", False, world.waypoints)

    #draw groups
    enemy_group.update()
    enemy_group.draw(screen)
    turret_group.draw(screen)

    

    for event in pygame.event.get():
        #Möglichkeit das Spiel zu beenden
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                create_turret(mouse_pos)

    pygame.display.flip()

pygame.quit()
