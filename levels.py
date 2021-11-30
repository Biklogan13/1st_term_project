import pygame

import enemies
import shuttle
import settings
import ammunition

buttons = []
screen = None
ammo_type = 1
super_charge = 0
level_background = None
bullets_indicator, plasma_indicator, laser_indicator = None, None, None

def init():
    global buttons, screen, level_background, bullets_indicator, plasma_indicator, laser_indicator
    screen = pygame.Surface(settings.SIZE)
    level_background = pygame.image.load('backgrounds/menu_background.png').convert_alpha()
    level_background = pygame.transform.scale(level_background, settings.SIZE)

    bullets_indicator = pygame.image.load('menu_images/weapon_indicator_bullets.png').convert_alpha()
    bullets_indicator = pygame.transform.scale(bullets_indicator, (350, 100))
    plasma_indicator = pygame.image.load('menu_images/weapon_indicator_plasma.png').convert_alpha()
    plasma_indicator = pygame.transform.scale(plasma_indicator, (350, 100))
    laser_indicator = pygame.image.load('menu_images/weapon_indicator_laser.png').convert_alpha()
    laser_indicator = pygame.transform.scale(laser_indicator, (350, 100))

    ammunition.processing(screen)


def blit_interface():
    global screen, bullets_indicator, bullets_indicator, plasma_indicator, laser_indicator
    # Weapon indicator
    if ammo_type == 0:
        screen.blit(bullets_indicator, (0, settings.HEIGHT - 100))
    elif ammo_type == 1:
        screen.blit(plasma_indicator, (0, settings.HEIGHT - 100))
    elif ammo_type == 2:
        screen.blit(laser_indicator, (0, settings.HEIGHT - 100))
    # Super indicator

def create_screen():
    global buttons, screen, ammo_type, level_background

    screen.blit(level_background, (0, 0))
    for b in buttons:
        b.draw(screen)
    for event in pygame.event.get():
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
    ammunition.processing(screen)
    enemies.processing(screen)
    shuttle.processing(screen)
    blit_interface()
    return screen


