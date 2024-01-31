# maingame.py
import pygame
import json
from enemy import Enemy
from turrets import Turret
from world import World
import constants as c
from turret_data import TURRET_DATA


# Initialisierung
pygame.init()
# Clock erstellen
clock = pygame.time.Clock()

# Variablen
blue = (0, 0, 255)
red = (255, 0, 0)
speed = c.TILE_SIZE
x, y = 0, 0

# Fenstereinstellungen treffen
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT + c.SIDE_PANEL))
pygame.display.set_caption("StarGuard")

# Gamevariables
attract_mode = True
game_over = False
game_outcome = 0
last_enemy_spawn = pygame.time.get_ticks()
placing_turrets = False
selected_turret = None
#Fonts
uheaval_font_small = pygame.font.Font("assets/UPHEAVTT.TTF", 25)
uheaval_font_big = pygame.font.Font("assets/UPHEAVTT.TTF", 40)

# load images
# cursor
cursor_image = pygame.image.load("levels/cursor.png").convert_alpha()
# map
map_image = pygame.image.load("levels/map_1.png").convert_alpha()

# turretTest SpriteSheet
turret_sheet_base = pygame.image.load(
    "assets/images/turrets/turret_1_new.png"
).convert_alpha()
turret_sheet_medium = pygame.image.load(
    "assets/images/turrets/turret_2_new.png"
).convert_alpha()
turret_sheet_strong = pygame.image.load(
    "assets/images/turrets/turret_3_new.png"
).convert_alpha()
# individual turret image for mouse cursor
cursor_turret = pygame.image.load(
    "assets/images/turrets/cursor_turret.png"
).convert_alpha()

turret_sheet = turret_sheet_base
turret_type = "base"
# enemies
enemy_images = {
    "weak": pygame.image.load("assets/images/enemies/enemy_1_s.png").convert_alpha(),
    "medium": pygame.image.load("assets/images/enemies/enemy_2_s.png").convert_alpha(),
    "strong": pygame.image.load("assets/images/enemies/enemy_3_s.png").convert_alpha(),
}

#turret icons
turret_icons = {
    "base": pygame.image.load("assets/images/turrets/base_turret_icon.png").convert_alpha(),
    "medium": pygame.image.load("assets/images/turrets/medium_turret_icon.png").convert_alpha(),
    "strong": pygame.image.load("assets/images/turrets/strong_turret_icon.png").convert_alpha()
}

current_turret_icon = turret_icons[f"{turret_type}"]

# Game Over Screen Image
game_over_image = pygame.image.load("assets/images/ZerstörtesRaumschiff.jpeg")
game_over_image = pygame.transform.scale(
    game_over_image, (c.SCREEN_HEIGHT, c.SCREEN_WIDTH)
)

# attract Mode
attract_mode_bg = pygame.image.load("assets/images/StarGuardBackGroundImage.jpeg")
attract_mode_bg = pygame.transform.scale(
    attract_mode_bg, (c.SCREEN_HEIGHT, c.SCREEN_WIDTH)
)
# Logo
attract_mode_logo = pygame.image.load("assets/images/LogoGepixelt.png")

# Heart,Coin and Textbox
heart_icon = pygame.image.load("assets/images/Heart.png")
coin_icon = pygame.image.load("assets/images/Coin.png")

heart_icon = pygame.transform.scale(heart_icon, (30, 30))
coin_icon = pygame.transform.scale(coin_icon, (30, 30))

# load json data for level
current_level = 1
with open(f"levels/map_{current_level}.tmj") as file:
    world_data = json.load(file)




# function for outputting text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# World Gruppe
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

# Turret Gruppe
turret_group = pygame.sprite.Group()


def create_turret():
    mouse_tile_x = x // c.TILE_SIZE
    mouse_tile_y = y // c.TILE_SIZE

    # calculate the sequential number of the tile
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x

    if world.tile_map[mouse_tile_num] == 99:
        # Check ob das Tile besetzt ist
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        # Wenn der Platz frei ist, dann setzen wir ein Turret
        if space_is_free == True:
            new_turret = Turret(turret_type, turret_sheet, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)
            # costs
            world.money -= c.BUY_COST


def select_turret():
    mouse_tile_x = x // c.TILE_SIZE
    mouse_tile_y = y // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret


# Enemy Gruppe
enemy_group = pygame.sprite.Group()
movement_timeout = 75
last_movement_time = pygame.time.get_ticks()

timer = 0
timer_abgelaufen = 1000
text_sichtbar = True

# game loop
run = True
while run:
    clock.tick(c.FPS)

    if attract_mode == True:
        screen.blit(attract_mode_bg, (0, 0))
        screen.blit(attract_mode_logo, (130, 100))
        timer += 30
        if timer >= timer_abgelaufen:
            timer = 0
            text_sichtbar = not text_sichtbar 
        
        if text_sichtbar:
            draw_text("Press G to start", uheaval_font_small, "grey100", 125, 350)
            

    else:
        screen.fill("grey100")
        world.draw(screen)

        pygame.draw.lines(screen, "grey0", False, world.waypoints)

        if game_over == False:
            if world.health <= 0:
                game_over = True
                game_outcome = -1  # Verloren

            # draw groups
            enemy_group.update(world)
            turret_group.update(enemy_group)

            # Highlight selected turret
            if selected_turret:
                if (
                    selected_turret.selected == False
                    or selected_turret.selected == None
                ):
                    selected_turret.selected = True


        enemy_group.draw(screen)
        for turret in turret_group:
            turret.draw(screen)

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
        # Ergenenzung, wennn der Spieler verliert:
        else:
            screen.blit(game_over_image, (0, 0))
            if game_outcome == -1:
                 timer += 30
                 if timer >= timer_abgelaufen:
                    timer = 0
                    text_sichtbar = not text_sichtbar 
                 if text_sichtbar:
                    draw_text("Game-Over", large_font, "white", 135, 190)
                    draw_text("Press R to restart", uheaval_font_small, "white", 121, 230)

    for event in pygame.event.get():
        # Möglichkeit das Spiel zu beenden
        if event.type == pygame.QUIT:
            run = False

    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and current_time - last_movement_time > movement_timeout:
        if y > 0:
            y -= speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()
    if keys[pygame.K_s] and current_time - last_movement_time > movement_timeout:
        if y < c.SCREEN_HEIGHT - c.TILE_SIZE:
            y += speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()
    if keys[pygame.K_a] and current_time - last_movement_time > movement_timeout:
        if x > 0:
            x -= speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()
    if keys[pygame.K_d] and current_time - last_movement_time > movement_timeout:
        if x < c.SCREEN_WIDTH - c.TILE_SIZE:
            x += speed
            last_movement_time = current_time
            if(selected_turret):
                selected_turret.selected = None
            selected_turret = select_turret()
    if keys[pygame.K_o] and current_time - last_movement_time > movement_timeout:
        # check if there is enough money
        if world.money >= c.BUY_COST:
            create_turret()
    if keys[pygame.K_g] and current_time - last_movement_time > movement_timeout:
        attract_mode = False

    if keys[pygame.K_l]:
        if keys[pygame.K_v] and current_time - last_movement_time > movement_timeout:
            # Switch between Turrets - right Strong Turret

            turret_sheet = turret_sheet_strong
            turret_type = "strong"
        if keys[pygame.K_c] and current_time - last_movement_time > movement_timeout:
            # Switch between Turrets - up Medium Turret
            turret_sheet = turret_sheet_medium
            turret_type = "medium"
        if keys[pygame.K_x] and current_time - last_movement_time > movement_timeout:
            # Switch between Turrets - left Base Turret
            turret_sheet = turret_sheet_base
            turret_type = "base"

    # Restart Option
    if keys[pygame.K_r] and game_over == True:
        game_over = False
        selected_turret = None
        last_enemy_spawn = pygame.time.get_ticks()
        world = World(world_data, map_image)
        world.process_data()
        world.process_enemies()
        enemy_group.empty()
        turret_group.empty()

    if attract_mode == False:
        screen.blit(cursor_image, (x, y))
    pygame.display.flip()

pygame.quit()
