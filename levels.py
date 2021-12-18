import pygame
import os
import copy

import enemies
import shuttle
import settings
import ammunition

pygame.init()

# Global variables of levels section
# Surface on which levels elements will be drown
screen = None
# An array which contains all Buttons objects
buttons = []
# Background of the levels section
level_background = None
# Type of selected ammo
ammo_type = 0
# Arrays which contain all images which will be displayed directly on screen
left_indicator = dict.fromkeys(['bullets', 'plasma', 'laser'])
right_indicator = dict.fromkeys(['plate', 'bar_edges', 'super_bar', 'super_bar_ready', 'hp_bar'])


def load_images():
    global level_background

    level_background_path = os.path.join('.', 'backgrounds', 'menu_background_1.png')
    level_background = pygame.image.load(level_background_path).convert_alpha()

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
    right_indicator['plate'] = indicator_plate

    indicator_edges_path = os.path.join('.', 'interface_elements', 'super_and_hp_indicator_edges.png')
    indicator_edges = pygame.image.load(indicator_edges_path).convert_alpha()
    right_indicator['bar_edges'] = indicator_edges

    super_bar_ready_path = os.path.join('.', 'interface_elements', 'super_bar_ready.png')
    super_bar_ready = pygame.image.load(super_bar_ready_path).convert_alpha()
    right_indicator['super_bar_ready'] = super_bar_ready

    super_bar_path = os.path.join('.', 'interface_elements', 'super_bar.png')
    super_bar = pygame.image.load(super_bar_path).convert_alpha()
    right_indicator['super_bar'] = super_bar

    hp_bar_path = os.path.join('.', 'interface_elements', 'hp_bar.png')
    hp_bar = pygame.image.load(hp_bar_path).convert_alpha()
    right_indicator['hp_bar'] = hp_bar


def red_image(image_original):
    image = copy.copy(image_original)
    # Making inverted mask
    mask = pygame.mask.from_surface(image)
    mask = mask.to_surface()
    mask_inv = pygame.Surface(mask.get_rect().size, pygame.SRCALPHA)
    mask_inv.fill((255, 255, 255, 255))
    mask_inv.blit(mask, (0, 0), None, pygame.BLEND_RGB_SUB)
    # Pouring image with red
    red = pygame.Surface(image.get_size()).convert_alpha()
    red.fill((255, 0, 0, 100))
    image.blit(red, (0, 0))
    # Deleting red edges of the picture which must be transparent
    image.blit(mask_inv, (0, 0), None, pygame.BLEND_RGB_MAX)
    image.set_colorkey((255, 255, 255))
    return image


def init():
    global screen

    # Creating screen and transforming images
    screen = pygame.Surface(settings.SIZE)

    super_and_hp_indicator = pygame.image.load(super_and_hp_indicator_path).convert_alpha()
    super_and_hp_indicator = pygame.transform.scale(super_and_hp_indicator, indicator_size)
    super_and_hp_indicator_edges = pygame.image.load(super_and_hp_indicator_edges_path).convert_alpha()
    super_and_hp_indicator_edges = pygame.transform.scale(super_and_hp_indicator_edges, indicator_size)
    hp_bar = pygame.image.load(hp_bar_path).convert_alpha()
    hp_bar = pygame.transform.scale(hp_bar, indicator_size)
    super_bar = pygame.image.load(super_bar_path).convert_alpha()
    super_bar = pygame.transform.scale(super_bar, indicator_size)
    super_bar_ready = pygame.image.load(super_bar_ready_path).convert_alpha()
    super_bar_ready = pygame.transform.scale(super_bar_ready, (265, 25))

    ammunition.init()


def blit_interface():
    global screen, bullets_indicator, bullets_indicator, plasma_indicator, laser_indicator, super_charge, \
        super_and_hp_indicator, super_and_hp_indicator_edges, hp_bar, super_bar, super_bar_ready
    # Weapon indicator
    if ammo_type == 0:
        screen.blit(bullets_indicator, (0, settings.HEIGHT - 100))
    elif ammo_type == 1:
        screen.blit(plasma_indicator, (0, settings.HEIGHT - 100))
    elif ammo_type == 2:
        screen.blit(laser_indicator, (0, settings.HEIGHT - 100))
    # Super and hp indicator
    screen.blit(super_and_hp_indicator, (settings.WIDTH - 350, settings.HEIGHT - 100))
    screen.blit(pygame.transform.scale(hp_bar, (265 * max(settings.spaceship.hp, 0) // settings.spaceship.max_hp, 25)),
                (settings.WIDTH - 350 + 135 // 2, settings.HEIGHT - 100 + 25 // 2))
    if settings.super_charge < 100:
        screen.blit(pygame.transform.scale(super_bar, (265 * settings.super_charge // 100, 25)),
                    (settings.WIDTH - 350 + 135 // 2, settings.HEIGHT - 100 + 125 // 2))
    else:
        screen.blit(super_bar_ready, (settings.WIDTH - 350 + 135 // 2, settings.HEIGHT - 100 + 125 // 2))
    screen.blit(super_and_hp_indicator_edges, (settings.WIDTH - 350, settings.HEIGHT - 100))


def create_screen():
    global buttons, screen, ammo_type, level_background

    screen.blit(level_background, (0, 0))
    for b in buttons:
        b.draw(screen)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                b.act(event)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            ammo_type = 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            ammo_type = 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            ammo_type = 2

        # Exiting to menu if esc is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        settings.flag = 'menu'
    ammunition.processing(screen, events)
    enemies.processing(screen)
    shuttle.processing(screen)
    blit_interface()
    return screen


