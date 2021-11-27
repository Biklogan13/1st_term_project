import pygame
import random
import menu
import shop
import levels
import shuttle
import ammunition
import settings

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
        self.x = random.randint(0, settings.WIDTH)
        self.y = -100
        self.Vx = 0
        self.Vy = 2
        self.live = 1
        self.image = None

    #def draw(self, screen):


    #def move(self):

#def init():


#def processing(screen):
