import pygame
import random
import settings

mine_image = None
enemy_counter = 0

class Enemy_standart:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = None
        self.r = 0

class Enemy_heavy:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = None
        self.r = 0

class Enemy_kamikaze:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = None
        self.r = 0

class Mine:
    def __init__(self):
        self.surface = None
        self.x = random.randint(25, settings.WIDTH - 25)
        self.y = -100
        self.Vx = 0
        self.Vy = 1
        self.live = 1
        self.image = mine_image
        self.r = 25

    def draw(self, screen):
        if self.live == 1:
            screen.blit(self.image, (self.x - 25, self.y - 25))

    def move(self):
        self.y += self.Vy

    def hittest(self, obj):
        if (self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2:
            return True
        else:
            return False

def init():
    global mine_image
    mine_image = pygame.image.load('enemy_skins/mine.png').convert_alpha()
    mine_image = pygame.transform.scale(mine_image, (50, 50))

def processing(screen):
    global enemy_counter
    if settings.tick_counter % 180 == 0:
        new_mine = Mine()
        enemy_counter += 1
        if len(settings.enemies) < 100:
            settings.enemies.append(new_mine)
        else:
            settings.enemies[enemy_counter % 100] = new_mine

    for k in settings.enemies:
        if k.hittest(settings.spaceship):
            k.live = 0

    for k in settings.enemies:
        k.draw(screen)
        k.move()