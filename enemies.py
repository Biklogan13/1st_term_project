import pygame

import menu
import shop
import levels
import shuttle
import ammunition
import enemies
import settings

class Enemy_standart:
    def __init__(self):
        self.surface = None
        self.x = 0
        self.y = 0
        self.Vx = 0
        self.Vy = 0
        self.live = 1
