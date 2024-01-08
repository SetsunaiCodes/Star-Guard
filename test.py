import pygame
import sys
import constants as c

pygame.init()
clock = pygame.time.Clock()

blue = (0,0,255)
red = (255,0,0)
speed = c.TILE_SIZE
x, y = 0, 0
currentColor = blue


screen = pygame.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGHT))
pygame.display.set_caption("Gird Controller")

movement_timeout = 75
last_movement_time = pygame.time.get_ticks()

run = True
while run:
    clock.tick(c.FPS)
    screen.fill("black")



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and current_time - last_movement_time > movement_timeout:
        if y > 0:
            y -= speed
            last_movement_time = current_time
    if keys[pygame.K_s] and current_time - last_movement_time > movement_timeout:
        if y < c.SCREEN_HEIGHT - c.TILE_SIZE:
            y += speed
            last_movement_time = current_time
    if keys[pygame.K_a] and current_time - last_movement_time > movement_timeout:
        if x > 0:
            x -= speed
            last_movement_time = current_time
    if keys[pygame.K_d] and current_time - last_movement_time > movement_timeout:
        if x < c.SCREEN_WIDTH - c.TILE_SIZE:
            x += speed
            last_movement_time = current_time        
    if keys[pygame.K_o] and current_time - last_movement_time > movement_timeout:
        currentColor = red if currentColor == blue else blue
        last_movement_time = current_time 

    pygame.draw.rect(screen, currentColor, (x, y, c.TILE_SIZE, c.TILE_SIZE))


    pygame.display.flip()

pygame.quit()
