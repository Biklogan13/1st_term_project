import pygame
import random
import settings
import math

kamikaze_image = None
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
        if random.randint(1, 2) == 1:
            self.x = -20
        else:
            self.x = settings.WIDTH + 20
        self.y = random.randint(15, settings.HEIGHT - 15)
        self.Vx = 0
        self.Vy = 0
        self.live = 1
        self.image = kamikaze_image
        self.angle = 0
        self.r = 22.5

    def draw(self, screen):
        if self.live == 1:
            self.image = rot_center(kamikaze_image, self.angle*360/(-2*math.pi) - 90)
            screen.blit(self.image, (self.x - 15, self.y - 15))

    def move(self):
        self.angle = math.atan2(settings.spaceship.y - self.y, settings.spaceship.x - self.x)
        self.Vx = math.cos(self.angle)
        self.Vy = math.sin(self.angle)
        self.x += self.Vx
        self.y += self.Vy

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False

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
    global mine_image, kamikaze_image
    mine_image = pygame.image.load('enemy_skins/mine.png').convert_alpha()
    mine_image = pygame.transform.scale(mine_image, (50, 50))
    kamikaze_image = pygame.image.load('enemy_skins/smalldrone_1.PNG').convert_alpha()
    kamikaze_image = pygame.transform.scale(kamikaze_image, (30, 45))

def processing(screen):
    global enemy_counter
    if settings.tick_counter % 180 == 0:
        new_mine = Mine()
        #nemy_counter += 1
        #if len(settings.enemies) < 100:
        settings.enemies.append(new_mine)
        #else:
        #settings.enemies[enemy_counter % 100] = new_mine
    if settings.tick_counter % 360 == 0:
        new_kamikaze = Enemy_kamikaze()
        #enemy_counter += 1
        #if len(settings.enemies) < 100:
        settings.enemies.append(new_kamikaze)
        #else:
        #settings.enemies[enemy_counter % 99] = new_kamikaze

    for k in settings.enemies:
        if k.hittest(settings.spaceship):
            k.live = 0
        for b in settings.bullets:
            if k.hittest(b):
                k.live = 0
        for p in settings.plasma_balls:
            if k.hittest(p):
                k.live = 0

    for k in settings.enemies:
        k.move()
        k.draw(screen)

def rot_center(image, angle):
    WIDTH = image.get_width()
    HEIGHT = image.get_height()
    orig_rect = image.get_rect(width=min(WIDTH, HEIGHT), height=min(WIDTH, HEIGHT))
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect()
    rot_rect.center = rot_image.get_rect().center
    print(orig_rect, rot_rect)
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image