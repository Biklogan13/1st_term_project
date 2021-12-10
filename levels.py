import pygame
import os

import enemies
import shuttle
import settings
import ammunition

buttons = []
screen = None
ammo_type = 0
level_background = None
bullets_indicator, plasma_indicator, laser_indicator = None, None, None
super_and_hp_indicator, super_and_hp_indicator_edges, hp_bar, super_bar, super_bar_ready = None, None, None, None, None

# Images paths
level_background_path = os.path.join('backgrounds/menu_background_2.jpg')

bullets_indicator_path = os.path.join('.', 'interface_elements', 'weapon_indicator_bullets.png')
plasma_indicator_path = os.path.join('.', 'interface_elements', 'weapon_indicator_plasma.png')
laser_indicator_path = os.path.join('.', 'interface_elements', 'weapon_indicator_laser.png')

super_and_hp_indicator_path = os.path.join('.', 'interface_elements', 'super_and_hp_indicator.png')
super_and_hp_indicator_edges_path = os.path.join('.', 'interface_elements', 'super_and_hp_indicator_edges.png')
hp_bar_path = os.path.join('.', 'interface_elements', 'hp_bar.png')
super_bar_path = os.path.join('.', 'interface_elements', 'super_bar.png')
super_bar_ready_path = os.path.join('.', 'interface_elements', 'super_bar_ready.png')


def init():
    global buttons, screen, level_background, bullets_indicator, plasma_indicator, laser_indicator,\
        super_and_hp_indicator, super_and_hp_indicator_edges, hp_bar, super_bar, super_bar_ready

    # Creating screen and transforming images
    screen = pygame.Surface(settings.SIZE)

    level_background = pygame.image.load(level_background_path).convert_alpha()
    level_background = pygame.transform.scale(level_background, settings.SIZE)

    indicator_size = (350, 100)

    bullets_indicator = pygame.image.load(bullets_indicator_path).convert_alpha()
    plasma_indicator = pygame.image.load(plasma_indicator_path).convert_alpha()
    laser_indicator = pygame.image.load(laser_indicator_path).convert_alpha()
    bullets_indicator = pygame.transform.scale(bullets_indicator, indicator_size)
    plasma_indicator = pygame.transform.scale(plasma_indicator, indicator_size)
    laser_indicator = pygame.transform.scale(laser_indicator, indicator_size)

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


