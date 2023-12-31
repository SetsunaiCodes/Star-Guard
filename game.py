import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Tower Defense Game')
        self.screen = pygame.display.set_mode((1280, 960))
        self.clock = pygame.time.Clock() 


    def run(self):
        while True:
            self.screen.fill((0,0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

Game().run()