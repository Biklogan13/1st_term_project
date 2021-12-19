import pygame
import os
import copy

import enemies
import shuttle
import settings
import ammunition


# --------------- Global variables of levels section ---------------


# Global variables of levels section
# Surface on which levels elements will be drown
screen = None

# Background of the levels section
level_background = None

# Type of selected ammo
ammo_type = 0

# Fonts
font, font_small = None, None

# Arrays which contain all images which will be displayed directly on screen
left_indicator = dict.fromkeys(['bullets', 'plasma', 'laser'])
right_indicator = dict.fromkeys(['plate', 'bar_edges', 'super_bar', 'super_bar_ready', 'hp_bar'])

# Variables for game over
game_over_timer, ship_explosion_frame = 0, 0
#ship_death = ammunition.ShipDeathAnimation(settings.spaceship.x, settings.spaceship.y)

# ---------------------- Secondary functions ----------------------


def red_image(image_original):
    """
    Makes given image more red (used to display damage-taking)
    :param image_original: pygame.image
    :return: original image with all its not transparent pixels covered with red
    """
    image = copy.copy(image_original)

    # Making inverted mask
    mask = pygame.mask.from_surface(image)
    mask = mask.to_surface()
    mask_inv = pygame.Surface(mask.get_rect().size, pygame.SRCALPHA)
    mask_inv.fill((255, 255, 255, 255))
    mask_inv.blit(mask, (0, 0), None, pygame.BLEND_RGB_SUB)

    # Filling image with red
    red = pygame.Surface(image.get_size()).convert_alpha()
    red.fill((255, 0, 0, 100))
    image.blit(red, (0, 0))

    # Deleting red edges of the picture which must be transparent
    image.blit(mask_inv, (0, 0), None, pygame.BLEND_RGB_MAX)
    image.set_colorkey((255, 255, 255))

    return image


# -------------------- Initialization functions --------------------


def load_images():
    """
    Loads all images which are going to be blit directly on screen.
    """
    global level_background

    level_background_path = os.path.join('.', 'backgrounds', 'menu_background_1.png')
    level_background = pygame.image.load(level_background_path).convert_alpha()
    level_background = pygame.transform.scale(level_background, settings.SIZE)

    indicator_size = (350, 100)

    # Loading images for left indicator
    bullets_indicator_path = os.path.join('.', 'interface_elements', 'weapon_indicator_bullets.png')
    bullets_indicator = pygame.image.load(bullets_indicator_path).convert_alpha()
    left_indicator['bullets'] = pygame.transform.scale(bullets_indicator, indicator_size)

    plasma_indicator_path = os.path.join('.', 'interface_elements', 'weapon_indicator_plasma.png')
    plasma_indicator = pygame.image.load(plasma_indicator_path).convert_alpha()
    left_indicator['plasma'] = pygame.transform.scale(plasma_indicator, indicator_size)

    laser_indicator_path = os.path.join('.', 'interface_elements', 'weapon_indicator_laser.png')
    laser_indicator = pygame.image.load(laser_indicator_path).convert_alpha()
    left_indicator['laser'] = pygame.transform.scale(laser_indicator, indicator_size)

    # Loading images for right indicator
    indicator_plate_path = os.path.join('.', 'interface_elements', 'super_and_hp_indicator.png')
    indicator_plate = pygame.image.load(indicator_plate_path).convert_alpha()
    right_indicator['plate'] = pygame.transform.scale(indicator_plate, indicator_size)

    indicator_edges_path = os.path.join('.', 'interface_elements', 'super_and_hp_indicator_edges.png')
    indicator_edges = pygame.image.load(indicator_edges_path).convert_alpha()
    right_indicator['bar_edges'] = pygame.transform.scale(indicator_edges, indicator_size)

    super_bar_ready_path = os.path.join('.', 'interface_elements', 'super_bar_ready.png')
    super_bar_ready = pygame.image.load(super_bar_ready_path).convert_alpha()
    right_indicator['super_bar_ready'] = pygame.transform.scale(super_bar_ready, (265, 25))

    super_bar_path = os.path.join('.', 'interface_elements', 'super_bar.png')
    super_bar = pygame.image.load(super_bar_path).convert_alpha()
    right_indicator['super_bar'] = super_bar

    hp_bar_path = os.path.join('.', 'interface_elements', 'hp_bar.png')
    hp_bar = pygame.image.load(hp_bar_path).convert_alpha()
    right_indicator['hp_bar'] = hp_bar


def init():
    """
    Loads all data necessary to display interface.
    """
    global screen
    screen = pygame.Surface(settings.SIZE)

    load_fonts()

    load_images()
    ammunition.init()


# ----------------- functions which create screen -----------------


def blit_indicators():
    """
    Draws left (weapon) and right (super and hp) indicators on the screen.
    """
    # Left indicator
    if ammo_type == 0:
        screen.blit(left_indicator['bullets'], (0, settings.HEIGHT - 100))
    elif ammo_type == 1:
        screen.blit(left_indicator['plasma'], (0, settings.HEIGHT - 100))
    elif ammo_type == 2:
        screen.blit(left_indicator['laser'], (0, settings.HEIGHT - 100))

    # Right indicator
    screen.blit(right_indicator['plate'], (settings.WIDTH - 350, settings.HEIGHT - 100))
    screen.blit(pygame.transform.scale(right_indicator['hp_bar'],
                (265 * max(settings.spaceship.hp, 0) // settings.spaceship.max_hp, 25)),
                (settings.WIDTH - 350 + 135 // 2, settings.HEIGHT - 100 + 25 // 2))

    if settings.super_charge < 100:
        screen.blit(pygame.transform.scale(right_indicator['super_bar'],
                    (265 * settings.super_charge // 100, 25)),
                    (settings.WIDTH - 350 + 135 // 2, settings.HEIGHT - 100 + 125 // 2))
    else:
        screen.blit(right_indicator['super_bar_ready'],
                    (settings.WIDTH - 350 + 135 // 2, settings.HEIGHT - 100 + 125 // 2))

    screen.blit(right_indicator['bar_edges'], (settings.WIDTH - 350, settings.HEIGHT - 100))


def load_fonts():
    """
    Loads all needed fonts.
    """
    global font, font_small

    font_path = os.path.join('.', 'interface_elements', 'Montserrat-Bold.ttf')
    font = pygame.font.Font(font_path, 70)
    font_small = pygame.font.Font(font_path, 30)


def game_over():
    """
    Explode your ship with nearby hostiles and coins
    gather half of your coins
    respawn in the middle of the screen
    """
    global game_over_timer, ship_explosion_frame
    settings.spaceship.Vx = settings.spaceship.Vy = 0
    screen.blit(font.render('YOUR SHIP WAS DESTROYED', True, (255, 255, 255)),
                (settings.WIDTH / 2 - 520, settings.HEIGHT / 2 - 50))
    screen.blit(font_small.render('you lost half of your coins', True, (255, 255, 255)),
                (settings.WIDTH / 2 - 175, settings.HEIGHT / 2 + 20))
    settings.spaceship.x = settings.WIDTH / 2
    settings.spaceship.y = settings.HEIGHT / 2
    game_over_timer += 1
    if ship_explosion_frame < 5:
        screen.blit(ammunition.ship_blow_a[ship_explosion_frame],
                    (settings.spaceship.x - settings.WIDTH / 2, settings.spaceship.y - settings.HEIGHT))
    if settings.tick_counter % 4 == 0 and ship_explosion_frame < 6:
        ship_explosion_frame += 1
    for k in settings.enemies:
        settings.enemies.remove(k)
    for c in settings.coins:
        settings.coins.remove(c)
    if game_over_timer == 1:
        settings.money = settings.money // 2
        ammunition.explosion_sound.play()
    if game_over_timer == 180:
        settings.spaceship.hp = settings.spaceship.max_hp
        ship_explosion_frame = 0
        game_over_timer = 0


def create_screen():
    """
    Defines the appearance and event processing of the game when player is in the menu (settings.flag == 'levels').
    :return: pygame.surface with the size of screen
    """
    global ammo_type

    # Drawing background
    screen.blit(level_background, (0, 0))

    # Processing events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            ammo_type = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            ammo_type = 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            ammo_type = 2

    # Exiting to menu if esc is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.flag = 'menu'

    # Processing in-game objects
    ammunition.processing(events)
    enemies.processing(screen)
    shuttle.processing(screen)

    # Drawing indicators
    blit_indicators()

    # Game over
    if settings.spaceship.hp <= 0:
        game_over()

    # Returning the screen which will be displayed
    return screen


