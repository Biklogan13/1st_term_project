import pygame
import random
import menu
import shop
import levels
import shuttle
import ammunition
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

class Enemy_heavy:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = None

class Enemy_kamikaze:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = None

class Mine:
    def __init__(self):
        self.surface = None
        self.x = random.randint(25, settings.WIDTH - 25)
        self.y = -100
        self.Vx = 0
        self.Vy = 2
        self.live = 1
        self.image = mine_image

    def draw(self, screen):
        screen.blit(self.image, (self.x - 25, self.y - 25))

    def move(self):
        self.y += self.Vy

def init():
    global mine_image
    mine_image = pygame.image.load('enemy_skins/mine.png').convert_alpha()
    mine_image = pygame.transform.scale(mine_image, (50, 50))

def processing(screen):
    global enemy_counter
    if settings.tick_counter % 60 == 0:
        new_mine = Mine()
        enemy_counter += 1
        if len(settings.enemies) < 20:
            settings.enemies.append(new_mine)
        else:
            settings.enemies[enemy_counter % 20] = new_mine

    for k in settings.enemies:
        k.draw(screen)
        k.move()