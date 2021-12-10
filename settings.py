import pygame
import os

# Global variables which needed in many files

# Flags and screen characteristics
SIZE, WIDTH, HEIGHT, flag, shop_section, running = 0, 0, 0, 'menu', 'ships', True

# Objects needed in various modules
current_skin, spaceship, enemies, tick_counter, enemy_bullets = None, None, [], 0, []
light_rings, bullets, laser, plasma_balls, ammo, = [], [], None, [], 0

# FIXME REMOVE from here!
bullet_image, light_ring_image, plasma_ball_sprites = None, None, []

# Game settings
seconds, bullets_firerate, plasma_balls_firerate, bullet_damage, plasma_ball_damage, laser_damage = 0, 10, 60, 20, 100, 1

# Skins
skins = []

# Money
money = 200

# Colors
RED = 0xFF0000
YELLOW = 0xFFC91F
ORANGE = (255, 165, 0)

# FIXME REMOVE from here!
PLASMA_1_PATH = os.path.join('.', 'ammo_sprites', 'plasma_1.png')
PLASMA_2_PATH = os.path.join('.', 'ammo_sprites', 'plasma_2.png')
PLASMA_3_PATH = os.path.join('.', 'ammo_sprites', 'plasma_3.png')

PLASMA_BULLET_PATH = os.path.join('.', 'ammo_sprites', 'plasma_bullet.png')
LIGHT_RING_PATH = os.path.join('.', 'ammo_sprites', 'lightring.png')

LASER_SOUND_PATH = os.path.join('.', 'Sounds', 'LaserLaserBeam EE136601_preview-[AudioTrimmer.com].mp3')
CANNONS_SOUND_PATH = os.path.join('.', 'Sounds', 'ES_Cannon Blast 4.mp3')
PLASMAGUN_SOUND_PATH = os.path.join('.', 'Sounds', 'plasma_gun_powerup_01.mp3')

MINE_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'mine.png')
KAMIKADZE_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'kamikaze.PNG')
ENEMY_IMAGE_PATH = os.path.join('.', 'enemy_skins', 'enemy.PNG')


# Common classes
class Button:
    def __init__(self, x, y, width, height, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.hover = False
        self.pressed = False
        self.image = None
        self.image_hover = None
        self.image_pressed = None

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
