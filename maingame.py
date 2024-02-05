# || maingame.py || Maindatei ||

#Imports
import pygame
import json
from enemy import Enemy
from turrets import Turret
from world import World
import constants as c
from turret_data import TURRET_DATA

# || Initarea der Maingame ||

# Initialisieren von PyGame
pygame.init()
clock = pygame.time.Clock()

# Fenstereinstellungen
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT + c.SIDE_PANEL))
pygame.display.set_caption("StarGuard")

# Variablen für das Spiel
attract_mode = True
game_over = False
game_outcome = 0
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None
blue = (0, 0, 255)
red = (255, 0, 0)
speed = c.TILE_SIZE
x, y = 0, 0
uheaval_font_small = pygame.font.Font("assets/UPHEAVTT.TTF", 25)
uheaval_font_big = pygame.font.Font("assets/UPHEAVTT.TTF", 40)

# || Laden von Bildern ||
cursor_image = pygame.image.load("levels/cursor.png").convert_alpha()
map_image = pygame.image.load("levels/map_1.png").convert_alpha()
turret_sheet_base = pygame.image.load( "assets/images/turrets/turret_1_new.png").convert_alpha()
turret_sheet_medium = pygame.image.load( "assets/images/turrets/turret_2_new.png").convert_alpha()
turret_sheet_strong = pygame.image.load( "assets/images/turrets/turret_3_new.png").convert_alpha()
cursor_turret = pygame.image.load( "assets/images/turrets/cursor_turret.png" ).convert_alpha()
attract_mode_logo = pygame.image.load("assets/images/LogoGepixelt.png")
heart_icon = pygame.image.load("assets/images/Heart.png")
coin_icon = pygame.image.load("assets/images/Coin.png")
heart_icon = pygame.transform.scale(heart_icon, (30, 30))
coin_icon = pygame.transform.scale(coin_icon, (30, 30))

turret_sheet = turret_sheet_base
turret_type = "base"

# Dictionaries
enemy_images = {
    "weak": pygame.image.load("assets/images/enemies/enemy_1_s.png").convert_alpha(),
    "medium": pygame.image.load("assets/images/enemies/enemy_2_s.png").convert_alpha(),
    "strong": pygame.image.load("assets/images/enemies/enemy_3_s.png").convert_alpha(),
}

turret_icons = {
    "base": pygame.image.load("assets/images/turrets/base_turret_icon.png").convert_alpha(),
    "medium": pygame.image.load("assets/images/turrets/medium_turret_icon.png").convert_alpha(),
    "strong": pygame.image.load("assets/images/turrets/strong_turret_icon.png").convert_alpha()
}
current_turret_icon = turret_icons[f"{turret_type}"]

#Background Images
game_over_image = pygame.image.load("assets/images/ZerstörtesRaumschiff.jpeg")
game_over_image = pygame.transform.scale(
    game_over_image, (c.SCREEN_HEIGHT, c.SCREEN_WIDTH)
)

attract_mode_bg = pygame.image.load("assets/images/StarGuardBackGroundImage.jpeg")
attract_mode_bg = pygame.transform.scale(
    attract_mode_bg, (c.SCREEN_HEIGHT, c.SCREEN_WIDTH)
)

# | Einladen der Level über JSON Dateien |
current_level = 1
with open(f"levels/map_{current_level}.tmj") as file:
    world_data = json.load(file)


# | Funktion um Text einzuzeigen |
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#  |Variablen: World generieren |
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# | Variablen: Turrets |
turret_group = pygame.sprite.Group()

# Funktion um Turrets zu erstellen
def create_turret():
    mouse_tile_x = x // c.TILE_SIZE
    mouse_tile_y = y // c.TILE_SIZE

    # Die sequentielle Zahl bestimmt aus X und Y definieren
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    if world.tile_map[mouse_tile_num] == 99:
        # Check ob das Tile besetzt ist
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False

        # Wenn der Platz frei ist, dann wird ein Turret gesetzt
        if space_is_free == True:
            new_turret = Turret(turret_type, turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

            # Nachdem ein ein Turret gesetzt wurde, muss das Geld abgezogen werden
            world.money -= c.BUY_COST

# Funktion um den Radius von Turrets zu markieren
def select_turret():
    mouse_tile_x = x // c.TILE_SIZE
    mouse_tile_y = y // c.TILE_SIZE

    #Markierte Turrets der Liste hinzufügen
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret


# | Variablen: Gegner |
enemy_group = pygame.sprite.Group()
movement_timeout = 75
last_movement_time = pygame.time.get_ticks()
timer = 0
timer_abgelaufen = 1000
text_sichtbar = True

# | Game-Loop |

run = True
while run:
    clock.tick(c.FPS)

    # Anzeigen des Attract Modes
    if attract_mode == True:
        screen.blit(attract_mode_bg, (0, 0))
        screen.blit(attract_mode_logo, (130, 100))
        timer += 30
        if timer >= timer_abgelaufen:
            timer = 0
            text_sichtbar = not text_sichtbar 
        if text_sichtbar:
            draw_text("Press G to start", uheaval_font_small, "grey100", 125, 350)
            
    # Das eigentliche Spiel
    else:
        screen.fill("grey100")
        world.draw(screen)

        # Spiel läuft (Spieler hat noch nicht verloren)
        if game_over == False:
            if world.health <= 0:
                game_over = True
                game_outcome = -1  # Spieler hat Verloren
            # Aktualisieren der Turrets und der Gegner
            enemy_group.update(world)
            turret_group.update(enemy_group)

            # Radius eines gesetztes Turrets
            if selected_turret:
                if (
                    selected_turret.selected == False
                    or selected_turret.selected == None
                ):
                    selected_turret.selected = True

        # Gegner auf dem Bildschirm anzeigen
        enemy_group.draw(screen)

        # Turrets aus der entsprechenden Gruppe anzeigen
        for turret in turret_group:
            turret.draw(screen)


        # | GUI des Spiels |
        screen.blit(heart_icon, (40, 5))
        screen.blit(coin_icon, (120, 5))
        draw_text("Level: ", uheaval_font_small, "grey100", 210, 7)
        draw_text(str(world.health), uheaval_font_small, "grey100", 75, 7)
        draw_text(str(world.money), uheaval_font_small, "grey100", 150, 7)
        draw_text(str(world.level), uheaval_font_small, "grey100", 295, 7)
        pygame.draw.rect(screen, "grey100",(c.SCREEN_WIDTH-60,5,32,32))
        screen.blit(turret_icons[f"{turret_type}"], (c.SCREEN_WIDTH-60, 5))


        if game_over == False:
            if pygame.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images)
                    # Gegner der Gruppe hinzufügen
                    enemy_group.add(enemy)
                    # Counter erhöhen
                    world.spawned_enemies += 1
                    last_enemy_spawn = pygame.time.get_ticks()

            world.check_level_complete()
            if world.level_complete == True:
                world.money += c.LEVEL_COMPLETE_REWARD
                world.level += 1
                selected_turret = None
                last_enemy_spawn = pygame.time.get_ticks()
                current_level += 1
                placing_turrets = False
                world.reset_level()
                turret_group.empty()
                world.image = pygame.image.load(
                    f"levels/map_{current_level}.png"
                ).convert_alpha()
                with open(f"levels/map_{current_level}.tmj") as file:
                    world.level_data = json.load(file)
                world.process_data()
                world.process_enemies()
                world.level_complete = False

        # | Anzeigen des Game-Over Bildschirms | 
        else:
            screen.blit(game_over_image, (0, 0))
            if game_outcome == -1:
                 timer += 30
                 if timer >= timer_abgelaufen:
                    timer = 0
                    text_sichtbar = not text_sichtbar 
                 if text_sichtbar:
                    draw_text("Game-Over", uheaval_font_big, "white", 135, 190)
                    draw_text("Press R to restart", uheaval_font_small, "white", 121, 230)

    # | Event-Handler |
    for event in pygame.event.get():

        # Möglichkeit das Spiel über das rote X zu beenden
        if event.type == pygame.QUIT:
            run = False

    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()

    #Cursor: Hoch
    if keys[pygame.K_w] and current_time - last_movement_time > movement_timeout:
        if y > 0:
            y -= speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()

    #Cursor: Runter
    if keys[pygame.K_s] and current_time - last_movement_time > movement_timeout:
        if y < c.SCREEN_HEIGHT - c.TILE_SIZE:
            y += speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()
    
    #Cursor: Links
    if keys[pygame.K_a] and current_time - last_movement_time > movement_timeout:
        if x > 0:
            x -= speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()
    
    #Cursor: Rechts
    if keys[pygame.K_d] and current_time - last_movement_time > movement_timeout:
        if x < c.SCREEN_WIDTH - c.TILE_SIZE:
            x += speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()

    # Turret platzieren
    if keys[pygame.K_o] and current_time - last_movement_time > movement_timeout:
        # Überprüfen, ob der Spieler genug Geld hat
        if world.money >= c.BUY_COST:
            create_turret()

    # Spiel starten
    if keys[pygame.K_g] and current_time - last_movement_time > movement_timeout:
        attract_mode = False

    # Zwischen den Turrets wechseln
    if keys[pygame.K_l] and current_time - last_movement_time > movement_timeout:
        if turret_type == "base":
            turret_sheet = turret_sheet_medium
            turret_type = "medium"
            last_movement_time = current_time

        elif turret_type == "medium":
            turret_sheet = turret_sheet_strong
            turret_type = "strong"
            last_movement_time = current_time

        elif turret_type == "strong":
            turret_sheet = turret_sheet_base
            turret_type = "base"
            last_movement_time = current_time
            


    # Spiel neustarten, wenn im Game-Screen
    if keys[pygame.K_r] and game_over == True:
        game_over = False
        selected_turret = None
        last_enemy_spawn = pygame.time.get_ticks()
        world = World(world_data, map_image)
        world.process_data()
        world.process_enemies()
        enemy_group.empty()
        turret_group.empty()

    # Cursor erst dann anzeigen, wenn das Spiel gestartet wurde
    if attract_mode == False:
        screen.blit(cursor_image, (x, y))
    pygame.display.flip()

pygame.quit()
