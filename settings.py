import pygame
import os

# Global variables which needed in many files

# Flags and screen characteristics
SIZE, WIDTH, HEIGHT = 0, 0, 0
flag = 'menu'
running = True
menu_background = None

# Objects needed in various modules
current_skin, spaceship = None, None
enemies, enemy_bullets, coins = [], [], []
tick_counter = 0
light_rings, bullets, laser, plasma_balls, ammo, = [], [], None, [], 0

# Game settings
seconds, bullets_firerate, plasma_balls_firerate, bullet_damage, plasma_ball_damage, laser_damage = 0, 10, 60, 20, 100, 1
standart_enemy_bullet_damage, standart_enemy_bullet_firerate, enemy_missile_damage = 20, 10, 10

# Skins
skins = []

# Super
super_charge = 100

# Money
money = 200000

# Colors
RED = 0xFF0000
YELLOW = 0xFFC91F
ORANGE = (255, 165, 0)

# Common classes
class Button:
    def __init__(self, x, y, width, height, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hover = False
        self.pressed = False
        self.image = None
        self.image_hover = None
        self.image_pressed = None
        self.action = action

    def check_mouse(self, event):
        return event.button == 1 and\
               0 <= event.pos[0] - self.x <= self.width and\
               0 <= event.pos[1] - self.y <= self.height

    def hover_test(self, event):
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            self.hover = True
        else:
            self.hover = False
