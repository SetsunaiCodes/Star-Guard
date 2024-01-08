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

#Variablen
blue = (0,0,255)
red = (255,0,0)
speed = c.TILE_SIZE
x, y = 0, 0
currentColor = blue

#Fenstereinstellungen treffen
screen = pygame.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL,c.SCREEN_HEIGHT))
pygame.display.set_caption("StarGuard")

#Gamebooleans
placing_turrets = False
selected_turret = None

#load images
#cursor
cursor_image = pygame.image.load('levels/cursor.png').convert_alpha()
#map
map_image = pygame.image.load('levels/map.png').convert_alpha()

#turretTest SpriteSheet
turret_sheet = pygame.image.load('assets/images/turrets/turret_1_new.png').convert_alpha()
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

#Turret Gruppe
turret_group = pygame.sprite.Group()

def create_turret():
    mouse_tile_x = x // c.TILE_SIZE
    mouse_tile_y = y // c.TILE_SIZE

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
            new_turret = Turret(turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret():
    mouse_tile_x = x // c.TILE_SIZE
    mouse_tile_y = y // c.TILE_SIZE
    for turret in turret_group:
        if(mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret    
#Enemy Gruppe
enemy_group = pygame.sprite.Group()


enemy = Enemy(world.waypoints, enemy_image)
 #Gegner der Gruppe hinzufügen
enemy_group.add(enemy)

movement_timeout = 75
last_movement_time = pygame.time.get_ticks()

#game loop
run = True
while run:
    clock.tick(c.FPS)
    screen.fill("grey100")

    world.draw(screen)

    pygame.draw.lines(screen, "grey0", False, world.waypoints)

    #draw groups
    enemy_group.update()
    turret_group.update(enemy_group)

    
    #Highlight selected turret
    if selected_turret:
        if selected_turret.selected == False or selected_turret.selected == None:
            selected_turret.selected = True
        else:
            selected_turret.selected = False



    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    

    for event in pygame.event.get():
        #Möglichkeit das Spiel zu beenden
        if event.type == pygame.QUIT:
            run = False
            
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and current_time - last_movement_time > movement_timeout:
        if y > 0:
            y -= speed
            last_movement_time = current_time
            selected_turret = select_turret()
    if keys[pygame.K_s] and current_time - last_movement_time > movement_timeout:
        if y < c.SCREEN_HEIGHT - c.TILE_SIZE:
            y += speed
            last_movement_time = current_time
            selected_turret = select_turret()
    if keys[pygame.K_a] and current_time - last_movement_time > movement_timeout:
        if x > 0:
            x -= speed
            last_movement_time = current_time
            selected_turret = select_turret()
    if keys[pygame.K_d] and current_time - last_movement_time > movement_timeout:
        if x < c.SCREEN_WIDTH - c.TILE_SIZE:
            x += speed
            last_movement_time = current_time
            selected_turret = select_turret()
    if keys[pygame.K_o] and current_time - last_movement_time > movement_timeout:
        create_turret()

    screen.blit(cursor_image, (x, y))

    pygame.display.flip()

pygame.quit()