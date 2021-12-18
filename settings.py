import pygame
import os

# Global variables which needed in many files

# Flags and screen characteristics
SIZE, WIDTH, HEIGHT = 0, 0, 0
flag, shop_section, running = 'menu', 'ships', True
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

    def act(self, event):
        global running, flag, shop_section
        if event.button == 1 and 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            if self.action == 'exit':
                pygame.quit()
                running = False
            elif self.action == 'switch_to_menu':
                flag = 'menu'
            elif self.action == 'switch_to_levels':
                flag = 'levels'
            elif self.action == 'switch_to_shop':
                flag = 'shop'
            elif self.action == 'switch_to_ships':
                shop_section = 'ships'
            elif self.action == 'switch_to_upgrades':
                shop_section = 'upgrades'
            elif self.action == 'switch_to_cosmetics':
                shop_section = 'cosmetics'

    def draw(self, screen):
        if self.image is None:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        elif self.pressed:
            screen.blit(self.image_pressed, (self.x, self.y))
        elif self.hover:
            screen.blit(self.image_hover, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def hover_test(self, event):
        if 0 <= event.pos[0] - self.x <= self.width and 0 <= event.pos[1] - self.y <= self.height:
            self.hover = True
        else:
            self.hover = False
