import pygame, sys, random
from object import *
from frog import *
from lane import *

class Game:
    def __init__(self, screen_dimension, screen_caption, screen_color):
        pygame.init()
        pygame.display.set_mode(screen_dimension)
        pygame.display.set_caption(screen_caption)

        self.screen_color = screen_color
        self.DISPLAY = pygame.display.get_surface()
         
        #sprite group
        self.object_group = pygame.sprite.Group()
        self.car_group = pygame.sprite.Group()
        self.river_group = pygame.sprite.Group()
        self.frog_group = pygame.sprite.Group()

        
        self.all_groups = [self.object_group, self.car_group, self.river_group, self.frog_group]

        self.river_speeds = {}
        self.assetSetup()

    def assetSetup(self):
        Object((0,0), (672, 768), "Tastatur/images/Background.png", self.object_group)

        # Grass
        for x in range(14):
            Object((x*48, 384), (48, 48), "Tastatur/images/Purple.png", self.object_group)
            Object((x*48, 672), (48, 48), "Tastatur/images/Purple.png", self.object_group)
        for x in range(28):
            Object((x*24, 72), (24, 72), "Tastatur/images/Green.png", self.object_group)
            
        # Lanes
        speeds = [-2.5, -2, -1.5, -1, -.5, .5, 1, 1.5, 2, 2.5]
        random.shuffle(speeds)

        # River lanes
        for y in range(5):
            y_pos = y*48 + 144
            new_lane = Lane((0, y_pos), self.river_group, speeds.pop(), "river")
            self.river_speeds[y_pos//48] = new_lane.speed

        # Street lanes
        for y in range(5):
            y_pos = y*48 + 432
            Lane((0, y_pos), self.car_group, speeds.pop(), "street")

        self.frog = Frog((336, 672), (48, 48), "Tastatur/images/Frogger_Up.png", self.frog_group, [self.car_group, self.river_group], self.river_speeds)
    def events(self):
        self.frog.keyups = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.escape_key()
                self.frog.keyups.append(event.key)

    def escape_key(self):
        current_time = pygame.time.get_ticks()
        escape_delay = 1000

        if hasattr(self, "last_escape_time"):
            time_elapsed = current_time - self.last_escape_time
            if time_elapsed < escape_delay:
                pygame.quit()
                sys.exit()
        self.last_escape_time  = current_time

    def update_sprites(self):
        for group in self.all_groups:
                for sprite in group:
                    sprite.update()

    def draw_sprites(self):
        for group in self.all_groups:
            group.draw(self.DISPLAY)
         

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.events()
            self.update_sprites()
            #self.DISPLAY.fill(self.screen_color)
            self.draw_sprites()
            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    game = Game((672, 768), 'Frogger Hausaufgaben', (0,0,0)) #14x16
    game.run()